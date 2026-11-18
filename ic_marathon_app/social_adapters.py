"""Adapters for Cisco OpenID Connect accounts."""

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_username
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .validators import validate_cec


CISCO_PROVIDER_ID = "cisco"
OIDC_PROVIDER = "openid_connect"
CISCO_EMAIL_DOMAIN = "cisco.com"


def cec_from_email(email):
    """Return the CEC username encoded in a Cisco corporate address."""
    return str(email or "").strip().lower().partition("@")[0]


def is_cisco_login(sociallogin):
    """Cisco OIDC is the only provider, matched by provider ID or base provider.

    allauth stores ``SocialAccount.provider`` as ``provider_id or provider``,
    so the value depends on the configured provider ID and its casing.
    """
    provider = (sociallogin.account.provider or "").lower()
    return provider in {CISCO_PROVIDER_ID, OIDC_PROVIDER}


def _claims(sociallogin):
    claims = sociallogin.account.extra_data
    return claims if isinstance(claims, dict) else {}


def _name_claims(claims):
    first_name = claims.get("given_name", "")
    last_name = claims.get("family_name", "")
    if first_name or last_name:
        return str(first_name), str(last_name)

    fullname = str(claims.get("fullname", "")).strip()
    if not fullname:
        return "", ""
    names = fullname.split()
    return names[0], " ".join(names[1:])


class CiscoSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Map Cisco claims to Django's User fields during social signup."""

    def is_open_for_signup(self, request, sociallogin):
        return is_cisco_login(sociallogin)

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        claims = _claims(sociallogin)
        first_name, last_name = _name_claims(claims)

        username = str(
            claims.get("uid")
            or claims.get("user")
            or claims.get("email", "").split("@")[0]
            or sociallogin.account.uid
        )
        user.username = username[: User._meta.get_field("username").max_length]
        user.email = str(claims.get("email") or user.email or "")
        user.first_name = first_name
        user.last_name = last_name
        return user


class CiscoAccountAdapter(DefaultAccountAdapter):
    """Local password signup, keyed on a Cisco corporate email address.

    Cisco SSO needs a DUO-enrolled device, so users on an unenrolled phone or
    laptop create a password account instead. They never type a username: the
    CEC is derived from the email they sign up with, because
    ``views.profile_wizard`` copies ``User.username`` into ``Profile.cec`` and
    a mistyped CEC silently breaks Webex notifications and partner workouts.
    """

    def is_open_for_signup(self, request):
        return True

    def clean_email(self, email):
        """Require a @cisco.com address that yields a usable CEC username.

        This hook is shared by signup, password reset and add-email, so it only
        validates the shape of the address. Rejecting an address whose CEC is
        already taken belongs to signup alone (see ``forms.CiscoSignupForm``),
        because for a password reset an existing account is the whole point.
        """
        email = str(super().clean_email(email) or "").strip().lower()

        if email.rpartition("@")[2] != CISCO_EMAIL_DOMAIN:
            raise ValidationError(
                "Please sign up with your Cisco email address "
                f"(<CEC>@{CISCO_EMAIL_DOMAIN})."
            )

        cec = cec_from_email(email)
        if not cec:
            raise ValidationError(
                f"Please include your CEC username before @{CISCO_EMAIL_DOMAIN}."
            )
        # Same rule as Profile.cec, so signup can never create a profile that
        # the wizard would reject.
        validate_cec(cec)
        return email

    def populate_username(self, request, user):
        """Use the CEC from the email, leaving an SSO-provided username alone."""
        if user_username(user):
            return super().populate_username(request, user)
        user_username(user, cec_from_email(user_email(user)))
