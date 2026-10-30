from allauth.account import views as allauth_views
from django.urls import path, re_path

from .views import (
    PrivateConfirmEmailView,
    PrivatePasswordResetView,
    ResendVerificationView,
    SessionConfirmEmailView,
)

urlpatterns = [
    path(
        "verification/confirm/<str:flow>/",
        SessionConfirmEmailView.as_view(),
        name="account_confirm_email_session",
    ),
    path("login/", allauth_views.login, name="account_login"),
    path("logout/", allauth_views.logout, name="account_logout"),
    path("signup/", allauth_views.signup, name="account_signup"),
    path("inactive/", allauth_views.account_inactive, name="account_inactive"),
    path(
        "confirm-email/",
        allauth_views.email_verification_sent,
        name="account_email_verification_sent",
    ),
    path(
        "verification/resend/",
        ResendVerificationView.as_view(),
        name="account_resend_verification",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        PrivateConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "password/reset/", allauth_views.password_reset, name="account_reset_password"
    ),
    path(
        "password/reset/done/",
        allauth_views.password_reset_done,
        name="account_reset_password_done",
    ),
    path(
        "password/reset/key/done/",
        allauth_views.password_reset_from_key_done,
        name="account_reset_password_from_key_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        PrivatePasswordResetView.as_view(),
        name="account_reset_password_from_key",
    ),
]
