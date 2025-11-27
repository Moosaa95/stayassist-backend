from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that reads the access token from cookies.
    """

    def authenticate(self, request):
        """
        Override the authenticate method to read the token from cookies if not in the header.
        """
        # First, try to get the token from the Authorization header (standard JWT approach)
        try:
            header = self.get_header(request)

            if header is None:
                # If no Authorization header, try to get the token from cookies
                raw_token = request.COOKIES.get(settings.AUTH_ACCESS_TOKEN_NAME)
            else:
                # If Authorization header exists, extract the token from it
                raw_token = self.get_raw_token(header)

            if raw_token is None:
                return None

            # Validate the token and return the user
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token

        except (InvalidToken, TokenError):
            return None
        except Exception:
            return None
