from django.urls import path

from apps.accounts.views.instructor.dashboard import (
    InstructorDashboardView,
)
from apps.accounts.views.instructor.students import (
    InstructorStudentListView,
    InstructorStudentDetailView,
)
from apps.accounts.views.instructor.student_attempts import (
    InstructorStudentAttemptsView,
)
from apps.accounts.views.instructor.attempt import (
    InstructorAttemptDetailView,
)


urlpatterns = [
    path(
        "instructor/dashboard/",
        InstructorDashboardView.as_view(),
        name="instructor-dashboard",
    ),
    path(
        "instructor/students/",
        InstructorStudentListView.as_view(),
        name="instructor-students",
    ),
    path(
        "instructor/students/<int:pk>/",
        InstructorStudentDetailView.as_view(),
        name="instructor-student-detail",
    ),
    path(
        "instructor/students/<int:pk>/attempts/",
        InstructorStudentAttemptsView.as_view(),
        name="instructor-student-attempts",
    ),
    path(
        "instructor/attempt/<uuid:pk>/",
        InstructorAttemptDetailView.as_view(),
        name="instructor-attempt-detail",
    ),
]
