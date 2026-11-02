from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

from .social_adapters import _name_claims, is_cisco_login


@receiver(pre_social_login)
def sync_cisco_user(request, sociallogin, **kwargs):
    """Keep an existing Cisco user's local fields aligned with OIDC claims."""
    if not is_cisco_login(sociallogin) or not sociallogin.user.pk:
        return

    claims = sociallogin.account.extra_data
    if not isinstance(claims, dict):
        return

    user = sociallogin.user
    first_name, last_name = _name_claims(claims)
    values = {
        "username": claims.get("uid") or claims.get("user"),
        "email": claims.get("email"),
        "first_name": first_name,
        "last_name": last_name,
    }

    changed_fields = []
    for field, value in values.items():
        if value and getattr(user, field) != value:
            setattr(user, field, str(value))
            changed_fields.append(field)

    if changed_fields:
        user.save(update_fields=changed_fields)
