from django.urls import path
from apps.accounts import views

urlpatterns = [
    # Authentication endpoints
    path("register/", views.RegisterView.as_view(), name="register"),
    path("token/", views.CustomTokenObtainView.as_view(), name="token_obtain_pair"),
    path(
        "token/refresh/",
        views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("token/verify/", views.CustomTokenVerifyView.as_view(), name="token_verify"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # User profile endpoints
    path("me/", views.CurrentUserView.as_view(), name="current_user"),
]
