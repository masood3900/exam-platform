from django.urls import path

from apps.accounts.views.profile.profile import (
    ProfileView,
)


urlpatterns = [

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),
]
