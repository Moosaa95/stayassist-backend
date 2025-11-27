from django.conf import settings
from django.db import IntegrityError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from accounts.utils import set_auth_cookies
from apps.accounts.serializers import (
    CustomTokenObtainPairSerializer,
    UserCreateSerializer,
    CustomUserSerializer,
)

# Create your views here.

class CustomTokenObtainView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # SimpleJWT returns 'access' and 'refresh' by default
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            if access_token and refresh_token:
                set_auth_cookies(response, access_token, refresh_token)

            response.data["status"] = True
        return response


class CustomTokenRefreshView(TokenRefreshView):
    """Handles token refresh by reading the refresh token from cookies if not provided in the request body."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        # Get refresh token from cookies
        refresh_token = request.COOKIES.get(settings.AUTH_REFRESH_TOKEN_NAME)

        # If no refresh token in request body, get it from cookies
        if not request.data.get('refresh') and refresh_token:
            # Make request.data mutable
            if hasattr(request.data, '_mutable'):
                request.data._mutable = True

            request.data['refresh'] = refresh_token

            if hasattr(request.data, '_mutable'):
                request.data._mutable = False


        response = super().post(request, *args, **kwargs)

        # Update cookies with new tokens if refresh was successful
        if response.status_code == 200:
            # SimpleJWT returns 'access' and 'refresh' by default
            access_token = response.data.get("access")
            new_refresh_token = response.data.get("refresh")  # May not exist if rotation is disabled

            if access_token:
                # If refresh token rotation is enabled, update both cookies
                if new_refresh_token:
                    set_auth_cookies(response, access_token, new_refresh_token)
                else:
                    # Keep existing refresh token
                    set_auth_cookies(response, access_token, refresh_token)

        return response



class CustomTokenVerifyView(TokenVerifyView):
    """
    Custom token verification view to handle token verification.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle token verification.
        """
        access_token = request.COOKIES.get(settings.AUTH_ACCESS_TOKEN_NAME)
        print("ACCESS VERIFY", access_token)
        if access_token:
            data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
            # SimpleJWT expects 'token' field for verification
            data['token'] = access_token
            request._full_data = data  # Override the request data safely

        return super().post(request, *args, **kwargs)
# class CustomTokenObtainView(TokenObtainPairView):

#     serializer_class = CustomTokenObtainPairSerializer

#     def post(self, request, *args, **kwargs):
#         print("RESULT", request.data)
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == 200:

#             access_token = response.data.get("access")
#             refresh_token = response.data.get("refresh")

#             if access_token and refresh_token:
#                 set_auth_cookies(response, access_token, refresh_token)

#             response.data["status"] = True
#         print("RESPONSE ", response)
#         return response


# class CustomTokenRefreshView(TokenRefreshView):
#     """Handles token refresh by reading the refresh token from cookies if not provided in the request body."""

#     def post(self, request, *args, **kwargs):
#         """Overrides the default post method to get the refresh token from cookies if not provided."""

#         # Get refresh token from cookies
#         refresh_token = request.COOKIES.get(settings.AUTH_REFRESH_TOKEN_NAME)

#         # Create mutable data copy
#         if hasattr(request.data, '_mutable'):
#             request.data._mutable = True

#         # Set refresh token in request data if not already present
#         if refresh_token and "refresh" not in request.data:
#             request.data["refresh"] = refresh_token

#         # Call the parent class's post method
#         response = super().post(request, *args, **kwargs)

#         # Update cookies with new tokens if refresh was successful
#         if response.status_code == 200:
#             access_token = response.data.get("access")
#             new_refresh_token = response.data.get("refresh")  # May not exist if rotation is disabled

#             if access_token:
#                 # If refresh token rotation is enabled, update both cookies
#                 if new_refresh_token:
#                     set_auth_cookies(response, access_token, new_refresh_token)
#                 else:
#                     # Keep existing refresh token
#                     set_auth_cookies(response, access_token, refresh_token)

#         return response


# class CustomTokenVerifyView(TokenVerifyView):
#     """
#     Custom token verification view to handle token verification.
#     """

#     def post(self, request, *args, **kwargs):
#         """
#         Handle token verification.
#         """
#         access_token = request.COOKIES.get(settings.AUTH_ACCESS_TOKEN_NAME)
#         if access_token:
#             data = request.data.copy()
#             data["access"] = access_token
#             request._full_data = data  # Override the request data safely

#         return super().post(request, *args, **kwargs)


# class RegisterView(APIView):
#     """
#     Handles user registration.
#     """

#     permission_classes = [AllowAny]

#     def post(self, request):
#         """Create a new user account."""
#         serializer = UserCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response(
#                 {
#                     "status": True,
#                     "message": "User registered successfully. Please check your email for verification.",
#                     "user": CustomUserSerializer(user).data,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(
#             {"status": False, "errors": serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST,
#         )


class RegisterView(generics.CreateAPIView):
    """
    API endpoint to register a new user.
    """

    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]  # Anyone can register

    def create(self, request):
        """
        Handle user registration.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully!",
                "user_id": user.id,
                "status": True,
                "user_email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutView(APIView):
    """
    Handles user logout by clearing authentication cookies.
    """

    def post(self, request):
        """Clear authentication cookies on logout."""
        response = Response(
            {"status": True, "message": "Logged out successfully"},
            status=status.HTTP_200_OK,
        )

        # Clear authentication cookies
        response.delete_cookie(
            settings.AUTH_ACCESS_TOKEN_NAME,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
        )
        response.delete_cookie(
            settings.AUTH_REFRESH_TOKEN_NAME,
            path=settings.AUTH_COOKIE_PATH,
            samesite=settings.AUTH_COOKIE_SAMESITE,
        )

        return response


class CurrentUserView(APIView):
    """
    Returns the currently authenticated user's information.
    """

    def get(self, request):
        """Get current user details."""
        serializer = CustomUserSerializer(request.user)
        return Response(
            {"status": True, "user": serializer.data}, status=status.HTTP_200_OK
        )
