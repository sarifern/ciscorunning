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

    first_name = None
    last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'] = self.fields.get('first_name', None) or self._create_char_field('First name')
        self.fields['last_name'] = self.fields.get('last_name', None) or self._create_char_field('Last name')

    def _create_char_field(self, label):
        from django import forms
        return forms.CharField(
            label=label,
            required=True,
            max_length=30,
            widget=forms.TextInput(attrs={'autocomplete': 'name'})
        )

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

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.save()
        return user
