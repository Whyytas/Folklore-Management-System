# from oauth2_provider.models import AccessToken
# from oauth2_provider.oauth2_validators import OAuth2Validator
# from oauthlib.oauth2.rfc6749.tokens import BearerToken
#
# class CustomBearerToken(BearerToken):
#     def create_token(self, request, token, user, *args, **kwargs):
#         token = super().create_token(request, token, user, *args, **kwargs)
#         if user:
#             role = getattr(user, 'role', 'default')
#             print(f"Role added to token: {role}")  # Debugging line
#             token['role'] = role
#         return token
#
#
# class CustomTokenSerializer(OAuth2Validator):
#     def validate_bearer_token(self, token, scopes, request):
#         validated = super().validate_bearer_token(token, scopes, request)
#         if validated and request.user:
#             token['role'] = getattr(request.user, 'role', 'default')  # Add role here too
#         return validated
