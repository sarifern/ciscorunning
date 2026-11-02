"""Adapters for Cisco OpenID Connect accounts."""

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User


CISCO_PROVIDER_ID = "cisco"
OIDC_PROVIDER = "openid_connect"


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
    """Disable local account authentication while retaining Cisco signup."""

    def is_open_for_signup(self, request):
        return False

    def authenticate(self, request, **credentials):
        return None
