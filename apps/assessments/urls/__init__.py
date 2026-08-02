from django.urls import include, path


urlpatterns = [
    path(
        "exam/",
        include("apps.assessments.urls.exam"),
    ),
]