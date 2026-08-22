from django.urls import path

from apps.accounts.views.admin.dashboard import (
    AdminDashboardView,
)

from apps.accounts.views.admin.courses import (
    AdminCourseListView,
)

from apps.accounts.views.admin.courses_create import (
    AdminCourseCreateView,
)

from apps.accounts.views.admin.courses_detail import (
    AdminCourseDetailView,
)

from apps.accounts.views.admin.learning_paths import (
    AdminLearningPathListView,
)

from apps.accounts.views.admin.learning_paths_create import (
    AdminLearningPathCreateView,
)

from apps.accounts.views.admin.learning_paths_detail import (
    AdminLearningPathDetailView,
)

from apps.accounts.views.admin.learning_paths_delete import (
    AdminLearningPathDeleteView,
)
from apps.accounts.views.admin.courses_update import (
    AdminCourseUpdateView,
)

from apps.accounts.views.admin.courses_toggle_active import (
    AdminCourseToggleActiveView,
)
from apps.accounts.views.admin.learning_paths_update import (
    AdminLearningPathUpdateView,
)


urlpatterns = [

    path(
        "dashboard/",
        AdminDashboardView.as_view(),
        name="admin-dashboard",
    ),

    path(
        "learning-paths/",
        AdminLearningPathListView.as_view(),
        name="admin-learning-paths",
    ),

    path(
        "learning-paths/create/",
        AdminLearningPathCreateView.as_view(),
        name="admin-learning-path-create",
    ),

    path(
        "learning-paths/<uuid:pk>/",
        AdminLearningPathDetailView.as_view(),
        name="admin-learning-path-detail",
    ),

    path(
        "learning-paths/<uuid:pk>/delete/",
        AdminLearningPathDeleteView.as_view(),
        name="admin-learning-path-delete",
    ),
    path(
        "learning-paths/<uuid:pk>/edit/",
        AdminLearningPathUpdateView.as_view(),
        name="admin-learning-path-update",
    ),

    path(
        "courses/",
        AdminCourseListView.as_view(),
        name="admin-courses",
    ),

    path(
        "courses/create/",
        AdminCourseCreateView.as_view(),
        name="admin-course-create",
    ),

    path(
        "courses/<uuid:pk>/",
        AdminCourseDetailView.as_view(),
        name="admin-course-detail",
    ),
    path(
        "courses/<uuid:pk>/toggle-active/",
        AdminCourseToggleActiveView.as_view(),
        name="admin-course-toggle-active",
    ),
    path(
        "courses/<uuid:pk>/edit/",
        AdminCourseUpdateView.as_view(),
        name="admin-course-edit",
    ),
]

