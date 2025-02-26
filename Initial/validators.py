from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.models import AccessToken
from datetime import timedelta
from django.utils.timezone import now


class CustomOAuth2Validator(OAuth2Validator):
    def save_bearer_token(self, token, request):
        super().save_bearer_token(token, request)
        if request.user:
            role = getattr(request.user, 'role', 'default')
            print(f"Adding role to token: {role}")  # Debugging log
            token['role'] = role
