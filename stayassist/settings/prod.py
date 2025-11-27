from .base import *
from os import getenv


AUTH_ACCESS_TOKEN_NAME = "access"
AUTH_REFRESH_TOKEN_NAME = "refresh"

# Cookie expiration time (in seconds)
AUTH_COOKIE_ACCESS_TOKEN_MAX_AGE = 60 * 15  # 15 minutes for access token
AUTH_COOKIE_REFRESH_TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # 7 days for refresh token

# Common Cookie Settings for Production (Cross-origin setup)
AUTH_COOKIE_PATH = "/"  # Available across the entire domain
AUTH_COOKIE_SECURE = True  # MUST be True in production (requires HTTPS)
AUTH_COOKIE_HTTP_ONLY = True  # Prevents JavaScript access (helps mitigate XSS)
AUTH_COOKIE_SAMESITE = "None"  # "None" is required for cross-origin cookies (Vercel frontend + Render backend)

# Production Security Settings
DEBUG = False
