from django.urls import path

from apps.accounts.views.profile.profile import (
    ProfileView,
)
from apps.accounts.views.profile.referrals import (
    ReferralsView,
)
from apps.accounts.views.profile.wallet import (
    WalletView,
)
from apps.accounts.views.profile.change_password import (
    ProfileChangePasswordView,
)


urlpatterns = [

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "referrals/",
        ReferralsView.as_view(),
        name="referrals",
    ),
    path(
        "wallet/",
        WalletView.as_view(),
        name="wallet",
    ),
    path(
        "change-password/",
        ProfileChangePasswordView.as_view(),
        name="change-password",
    ),
]
