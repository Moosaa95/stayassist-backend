from .base import *
from os import getenv


AUTH_ACCESS_TOKEN_NAME = "access"
AUTH_REFRESH_TOKEN_NAME = "refresh"

# Cookie expiration time (in seconds)
AUTH_COOKIE_ACCESS_TOKEN_MAX_AGE = 60 * 15  # 15 minutes for access token
AUTH_COOKIE_REFRESH_TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # 7 days for refresh token

# Common Cookie Settings
AUTH_COOKIE_PATH = "/"  # Available across the entire domain
AUTH_COOKIE_SECURE = getenv("AUTH_COOKIE_SECURE", "False") == "True"  # False for local (http), True for production (https)
AUTH_COOKIE_HTTP_ONLY = True  # Prevents JavaScript access (helps mitigate XSS)
AUTH_COOKIE_SAMESITE = getenv("AUTH_COOKIE_SAMESITE", "Lax")  # "None" for cross-origin, "Lax" for same-origin 
