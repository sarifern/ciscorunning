from io import BytesIO

from allauth.socialaccount.adapter import get_adapter as get_socialaccount_adapter
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.models import SocialLogin
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import (
	FSPartnerWorkoutForm,
	PartnerWorkoutConfirmationForm,
	PartnerWorkoutForm,
)
from .signals import sync_cisco_user
from .social_adapters import CiscoAccountAdapter, CiscoSocialAccountAdapter


CISCO_CLAIMS = {
	"amr": ["mfa", "pop", "user"],
	"sub": "28b43764bdb6c443d8972d06c64baaedf203212110148919f4c155c160b79024",
	"uid": "sarifern",
	"user": "sarifern",
	"email": "sarifern@cisco.com",
	"fullname": "Sari Fernandez (sarifern)",
	"given_name": "Sari",
	"family_name": "Fernandez",
}


def make_test_image(name="evidence.png"):
	image_data = BytesIO()
	Image.new("RGB", (2, 2), color="white").save(image_data, format="PNG")
	return SimpleUploadedFile(name, image_data.getvalue(), content_type="image/png")


class PartnerWorkoutEvidenceFormTests(SimpleTestCase):
	def test_submitter_evidence_is_required_and_selfie_is_optional(self):
		for form_class in (PartnerWorkoutForm, FSPartnerWorkoutForm):
			with self.subTest(form=form_class.__name__):
				form = form_class()
				self.assertTrue(form.fields["photo_evidence"].required)
				self.assertFalse(form.fields["partner_selfie"].required)

	def test_partner_evidence_is_always_required(self):
		form = PartnerWorkoutConfirmationForm(data={}, files={})

		self.assertFalse(form.is_valid())
		self.assertIn("partner_photo_evidence", form.errors)

	def test_partner_must_supply_selfie_only_when_submitter_did_not(self):
		required_form = PartnerWorkoutConfirmationForm(
			data={},
			files={"partner_photo_evidence": make_test_image()},
			require_selfie=True,
		)
		optional_form = PartnerWorkoutConfirmationForm(
			data={},
			files={"partner_photo_evidence": make_test_image()},
			require_selfie=False,
		)

		self.assertFalse(required_form.is_valid())
		self.assertIn("partner_selfie", required_form.errors)
		self.assertTrue(optional_form.is_valid(), optional_form.errors)


class CiscoSocialAccountAdapterTests(SimpleTestCase):
	def test_populate_user_maps_cisco_claims_to_django_fields(self):
		sociallogin = SocialLogin(
			user=User(),
			account=SocialAccount(
				provider="Cisco",
				uid=CISCO_CLAIMS["sub"],
				extra_data=CISCO_CLAIMS,
			)
		)

		user = CiscoSocialAccountAdapter().populate_user(None, sociallogin, {})

		self.assertEqual(sociallogin.account.uid, CISCO_CLAIMS["sub"])
		self.assertEqual(user.username, CISCO_CLAIMS["uid"])
		self.assertEqual(user.email, CISCO_CLAIMS["email"])
		self.assertEqual(user.first_name, CISCO_CLAIMS["given_name"])
		self.assertEqual(user.last_name, CISCO_CLAIMS["family_name"])

	def test_only_cisco_social_accounts_can_sign_up(self):
		adapter = CiscoSocialAccountAdapter()
		foreign_login = SocialLogin(account=SocialAccount(provider="strava"))

		for provider_id in ("Cisco", "cisco", "openid_connect"):
			with self.subTest(provider=provider_id):
				cisco_login = SocialLogin(account=SocialAccount(provider=provider_id))
				self.assertTrue(adapter.is_open_for_signup(None, cisco_login))

		self.assertFalse(adapter.is_open_for_signup(None, foreign_login))

	def test_local_account_signup_and_authentication_are_disabled(self):
		adapter = CiscoAccountAdapter()

		self.assertFalse(adapter.is_open_for_signup(None))
		self.assertIsNone(
			adapter.authenticate(
				None,
				username=CISCO_CLAIMS["uid"],
				password="not-used",
			)
		)


class CiscoExistingUserSyncTests(TestCase):
	def test_existing_cisco_user_is_updated_from_current_claims(self):
		user = User.objects.create_user(
			username="old-username",
			email="old-email@example.com",
			first_name="Old",
			last_name="Name",
		)
		sociallogin = SocialLogin(
			user=user,
			account=SocialAccount(
				user=user,
				provider="Cisco",
				uid=CISCO_CLAIMS["sub"],
				extra_data=CISCO_CLAIMS,
			),
		)

		sync_cisco_user(None, sociallogin)
		user.refresh_from_db()

		self.assertEqual(user.username, CISCO_CLAIMS["uid"])
		self.assertEqual(user.email, CISCO_CLAIMS["email"])
		self.assertEqual(user.first_name, CISCO_CLAIMS["given_name"])
		self.assertEqual(user.last_name, CISCO_CLAIMS["family_name"])

	def test_non_cisco_account_does_not_update_user(self):
		user = User.objects.create_user(username="unchanged")
		sociallogin = SocialLogin(
			user=user,
			account=SocialAccount(
				user=user,
				provider="strava",
				uid=CISCO_CLAIMS["sub"],
				extra_data=CISCO_CLAIMS,
			),
		)

		sync_cisco_user(None, sociallogin)
		user.refresh_from_db()

		self.assertEqual(user.username, "unchanged")


class CiscoOnlyAuthenticationTests(TestCase):
	def test_allauth_password_login_rejects_valid_local_credentials(self):
		user = User.objects.create_user(
			username="local-user",
			email="local-user@example.com",
			password="valid-local-password",
		)

		self.client.post(
			reverse("account_login"),
			{
				"login": user.username,
				"password": "valid-local-password",
			},
		)

		self.assertNotIn("_auth_user_id", self.client.session)

	def test_allauth_local_signup_does_not_create_user(self):
		self.client.post(
			reverse("account_signup"),
			{
				"username": "local-signup",
				"email": "local-signup@example.com",
				"password1": "not-a-real-password-123",
				"password2": "not-a-real-password-123",
			},
		)

		self.assertFalse(User.objects.filter(username="local-signup").exists())


class CiscoProviderConfigurationTests(TestCase):
	"""Guard the admin-configured Cisco app against duplicate/missing app errors."""

	def _create_admin_configured_app(self):
		return SocialApp.objects.create(
			provider="openid_connect",
			provider_id="Cisco",
			name="Cisco",
			client_id="DIK4A7USDFBT0E6MMR27",
			secret="test-secret",
			settings={
				"server_url": "https://sso-dbbfec7f.sso.duosecurity.com/oidc/DIK4A7USDFBT0E6MMR27"
			},
		)

	def test_admin_configured_app_resolves_without_duplicates(self):
		app = self._create_admin_configured_app()

		with override_settings(
			SOCIALACCOUNT_PROVIDERS={"openid_connect": {"APPS": []}}
		):
			resolved = get_socialaccount_adapter().get_app(None, provider="Cisco")

		self.assertEqual(resolved.pk, app.pk)

	def test_duplicate_admin_and_settings_apps_are_rejected(self):
		self._create_admin_configured_app()
		duplicate_settings = {
			"openid_connect": {
				"APPS": [
					{
						"provider_id": "Cisco",
						"name": "Cisco",
						"client_id": "DIK4A7USDFBT0E6MMR27",
						"secret": "test-secret",
						"settings": {"server_url": "https://example.test/oidc"},
					}
				]
			}
		}

		with override_settings(SOCIALACCOUNT_PROVIDERS=duplicate_settings):
			with self.assertRaises(MultipleObjectsReturned):
				get_socialaccount_adapter().get_app(None, provider="Cisco")

	def test_login_url_uses_the_configured_provider_id(self):
		self.assertEqual(
			reverse("openid_connect_login", kwargs={"provider_id": "Cisco"}),
			"/accounts/Cisco/login/",
		)
