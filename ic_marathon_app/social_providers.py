"""Custom provider adapters for django-allauth social login.

These override the stock adapters to log the raw provider response and fail
gracefully (via OAuth2Error, which allauth already catches and turns into a
friendly error page) instead of crashing with an unhandled 500 when the
provider's API returns an unexpected payload (e.g. rate limiting, a revoked
token, or a permissions issue).
"""
import logging

import requests
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from allauth.socialaccount.providers.strava.provider import StravaProvider

logger = logging.getLogger(__name__)


class StravaOauth2Adapter(OAuth2Adapter):
    provider_id = StravaProvider.id
    access_token_url = "https://www.strava.com/oauth/token"
    authorize_url = "https://www.strava.com/oauth/authorize"
    profile_url = "https://www.strava.com/api/v3/athlete"

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "Bearer {}".format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        if "id" not in extra_data:
            # Strava returned an error payload (e.g. rate limiting, a revoked
            # token, or a missing permission) instead of athlete data. Log the
            # raw response so the real cause is visible in the server logs,
            # and fail gracefully instead of crashing with a 500.
            logger.error(
                "Strava profile fetch failed (status=%s): %s",
                resp.status_code,
                extra_data,
            )
            raise OAuth2Error(
                "Strava did not return athlete data (status {}): {}".format(
                    resp.status_code, extra_data.get("message", "unknown error")
                )
            )
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(StravaOauth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(StravaOauth2Adapter)
