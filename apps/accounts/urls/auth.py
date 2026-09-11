from django.contrib.auth import views as auth_views
from django.urls import path

from apps.accounts.views.auth.login import UserLoginView
from apps.accounts.views.auth.register import RegisterView
from apps.accounts.views.auth.password_reset import PasswordResetRequestView, PasswordResetConfirmView


urlpatterns = [
    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "password-reset/",
        PasswordResetRequestView.as_view(),
        name="password-reset",
    ),
    path(
        "password-reset-confirm/<str:uidb64>/<str:token>/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
