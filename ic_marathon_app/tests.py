from io import BytesIO

import re

from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .forms import CiscoSignupForm
from .models import (
	FSPartnerWorkoutForm,
	PartnerWorkoutConfirmationForm,
	PartnerWorkoutForm,
	Profile,
	cute_avatar_url,
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


class ProfileAvatarTests(TestCase):
	def test_new_profile_gets_stable_cute_avatar(self):
		user = User.objects.create_user(username="avatar-user")

		profile = Profile.objects.create(user=user)
		profile.save()
		profile.refresh_from_db()

		self.assertEqual(profile.avatar, cute_avatar_url(user.pk))
		self.assertNotIn(user.username, profile.avatar)

	def test_custom_avatar_is_preserved(self):
		user = User.objects.create_user(username="custom-avatar-user")
		custom_avatar = "https://cdn.example.com/custom.png"

		profile = Profile.objects.create(user=user, avatar=custom_avatar)
		profile.save()
		profile.refresh_from_db()

		self.assertEqual(profile.avatar, custom_avatar)


class CiscoLocalSignupAdapterTests(TestCase):
	"""The CEC is derived from the Cisco email, never typed by the user."""

	def setUp(self):
		self.adapter = CiscoAccountAdapter()

	def test_local_signup_is_open(self):
		self.assertTrue(self.adapter.is_open_for_signup(None))

	def test_cisco_email_is_normalised(self):
		self.assertEqual(
			self.adapter.clean_email("  SariFern@Cisco.com  "),
			"sarifern@cisco.com",
		)

	def test_non_cisco_email_is_rejected(self):
		for email in ("sarifern@gmail.com", "sarifern@cisco.com.evil.com", "sarifern"):
			with self.subTest(email=email):
				with self.assertRaises(ValidationError):
					self.adapter.clean_email(email)

	def test_employee_number_is_rejected(self):
		with self.assertRaises(ValidationError):
			self.adapter.clean_email("123456@cisco.com")

	def test_existing_cec_is_rejected(self):
		User.objects.create_user(username="sarifern")

		form = CiscoSignupForm(
			{
				"email": "SariFern@cisco.com",
				"password1": PASSWORD,
				"password2": PASSWORD,
			}
		)

		self.assertFalse(form.is_valid())
		self.assertIn("email", form.errors)

	def test_adapter_does_not_reject_an_existing_cec(self):
		"""clean_email is shared with password reset, where the user exists."""
		User.objects.create_user(username="sarifern")

		self.assertEqual(
			self.adapter.clean_email("sarifern@cisco.com"),
			"sarifern@cisco.com",
		)

	def test_username_is_derived_from_the_cisco_email(self):
		user = User(email="sarifern@cisco.com")

		self.adapter.populate_username(None, user)

		self.assertEqual(user.username, "sarifern")

	def test_sso_supplied_username_is_left_alone(self):
		"""Social signup calls populate_username after setting the uid."""
		user = User(username="sarifern", email="sari.fernandez@cisco.com")

		self.adapter.populate_username(None, user)

		self.assertEqual(user.username, "sarifern")


PASSWORD = "a-strong-passphrase-42"


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class CiscoLocalSignupFlowTests(TestCase):
	"""End-to-end signup for users whose device is not enrolled in DUO."""

	def _signup(self, email=" SariFern@Cisco.com "):
		return self.client.post(
			reverse("account_signup"),
			{"email": email, "password1": PASSWORD, "password2": PASSWORD},
		)

	def test_signup_creates_a_user_whose_username_is_the_cec(self):
		self._signup()

		user = User.objects.get(email="sarifern@cisco.com")
		self.assertEqual(user.username, "sarifern")

	def test_signup_sends_a_confirmation_email(self):
		self._signup()

		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].to, ["sarifern@cisco.com"])

	def test_signup_rejects_a_non_cisco_email(self):
		self._signup(email="sarifern@gmail.com")

		self.assertFalse(User.objects.filter(email="sarifern@gmail.com").exists())

	def test_unconfirmed_signup_cannot_log_in(self):
		self._signup()
		self.client.logout()

		self.client.post(
			reverse("account_login"),
			{"login": "sarifern", "password": PASSWORD},
		)

		self.assertNotIn("_auth_user_id", self.client.session)

	def test_confirmed_user_logs_in_with_cec_or_cisco_email(self):
		user = User.objects.create_user(
			username="sarifern",
			email="sarifern@cisco.com",
			password=PASSWORD,
		)
		EmailAddress.objects.create(
			user=user,
			email=user.email,
			verified=True,
			primary=True,
		)

		for login_value in ("sarifern", "sarifern@cisco.com"):
			with self.subTest(login=login_value):
				self.client.logout()

				self.client.post(
					reverse("account_login"),
					{"login": login_value, "password": PASSWORD},
				)

				self.assertEqual(
					self.client.session.get("_auth_user_id"),
					str(user.pk),
				)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class SsoUserPasswordResetTests(TestCase):
	"""An SSO user needs a password to sign in from a device without DUO.

	They cannot sign up again (the CEC is taken), so the reset flow is the
	self-serve route. SSO accounts have an unusable password, which must not
	stop the reset email from being sent.
	"""

	def setUp(self):
		self.user = User.objects.create_user(
			username="ssouser",
			email="ssouser@cisco.com",
		)
		self.user.set_unusable_password()
		self.user.save()
		EmailAddress.objects.create(
			user=self.user,
			email=self.user.email,
			verified=True,
			primary=True,
		)

	def test_signup_points_an_existing_cec_at_the_reset_flow(self):
		form = CiscoSignupForm(
			{
				"email": "ssouser@cisco.com",
				"password1": PASSWORD,
				"password2": PASSWORD,
			}
		)

		self.assertFalse(form.is_valid())
		self.assertIn("password reset", " ".join(form.errors["email"]))

	def test_reset_emails_a_user_with_an_unusable_password(self):
		response = self.client.post(
			reverse("account_reset_password"),
			{"email": "ssouser@cisco.com"},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].to, ["ssouser@cisco.com"])

	def test_reset_link_sets_a_password_that_then_logs_in(self):
		self.client.post(
			reverse("account_reset_password"),
			{"email": "ssouser@cisco.com"},
		)
		link = re.search(
			r"https?://\S+/password/reset/key/\S+",
			mail.outbox[0].body,
		).group(0)

		# allauth swaps the key for a session-held one and redirects.
		response = self.client.get(link, follow=True)
		self.client.post(
			response.redirect_chain[-1][0] if response.redirect_chain else link,
			{"password1": PASSWORD, "password2": PASSWORD},
		)

		self.user.refresh_from_db()
		self.assertTrue(self.user.has_usable_password())

		self.client.logout()
		self.client.post(
			reverse("account_login"),
			{"login": "ssouser", "password": PASSWORD},
		)
		self.assertEqual(
			self.client.session.get("_auth_user_id"),
			str(self.user.pk),
		)

