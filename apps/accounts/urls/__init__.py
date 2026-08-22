from django.urls import include, path

app_name = "accounts"
urlpatterns = [
    path(
        "",
        include("apps.accounts.urls.auth"),
    ),

    path(
        "admin/",
        include("apps.accounts.urls.admin"),
    ),

    path(
        "",
        include("apps.accounts.urls.student"),
    ),

    path(
        "",
        include("apps.accounts.urls.instructor"),
    ),

    path(
        "",
        include("apps.accounts.urls.profile"),
    ),
]
