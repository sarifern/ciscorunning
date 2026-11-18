"""Account forms for Cisco local signup.

Kept out of ``models.py`` so allauth's forms are imported lazily, via the
``ACCOUNT_FORMS`` setting, rather than while the app registry is still loading.
"""

from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .social_adapters import cec_from_email


class CiscoSignupForm(SignupForm):
    """Signup keyed on a Cisco address, rejecting a CEC that already exists.

    The duplicate check lives here rather than in
    ``CiscoAccountAdapter.clean_email`` because that hook is shared with the
    password reset form, where an existing account is required rather than an
    error.
    """

    def clean_email(self):
        email = super().clean_email()
        cec = cec_from_email(email)

        if cec and User.objects.filter(username__iexact=cec).exists():
            raise ValidationError(
                f"An account already exists for CEC '{cec}'. Sign in with Cisco, "
                "or use the password reset link to set a password you can use "
                "on a device without DUO."
            )
        return email
