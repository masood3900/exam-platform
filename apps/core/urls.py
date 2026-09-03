from django.urls import path

from apps.core.views import (
    HomeView,
    CourseListView,
    AssessmentListView,
    AssessmentDetailView,
    CourseDetailPublicView,
)

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("courses/", CourseListView.as_view(), name="courses"),
    path("assessments/", AssessmentListView.as_view(), name="assessments"),
    path("assessments/<uuid:assessment_id>/", AssessmentDetailView.as_view(), name="assessment-detail"),
    path("courses/<uuid:pk>/", CourseDetailPublicView.as_view(), name="course-public-detail"),
]