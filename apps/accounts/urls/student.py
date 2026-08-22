from django.urls import path

from apps.accounts.views.student.dashboard import (
    DashboardView,
)

from apps.accounts.views.student.learning_path import (
    LearningPathDetailView,
)

from apps.accounts.views.student.course import (
    CourseDetailView,
)

from apps.accounts.views.student.category import (
    QuestionCategoryDetailView,
)

from apps.accounts.views.student.learning_objective import (
    LearningObjectiveDetailView,
)

from apps.accounts.views.student.course_enroll import (
    CourseEnrollView,
)


urlpatterns = [

    path(
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard",
    ),

    path(
        "dashboard/path/<uuid:pk>/",
        LearningPathDetailView.as_view(),
        name="learning-path-detail",
    ),

    path(
        "dashboard/path/<uuid:path_pk>/course/<uuid:pk>/",
        CourseDetailView.as_view(),
        name="course-detail",
    ),

    path(
        "dashboard/path/<uuid:path_pk>/course/<uuid:course_pk>/category/<uuid:pk>/",
        QuestionCategoryDetailView.as_view(),
        name="category-detail",
    ),

    path(
        "dashboard/path/<uuid:path_pk>/course/<uuid:course_pk>/category/<uuid:category_pk>/objective/<uuid:pk>/",
        LearningObjectiveDetailView.as_view(),
        name="learning-objective-detail",
    ),

    path(
        "course/<uuid:pk>/enroll/",
        CourseEnrollView.as_view(),
        name="course-enroll",
    ),
]
