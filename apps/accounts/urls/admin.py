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
from apps.accounts.views.admin.assessment_create import (
    AssessmentCreateView,
)
from apps.accounts.views.admin.assessment_rule_create import (
    AssessmentRuleCreateView,
)

from apps.accounts.views.admin.payment_review import PaymentReviewView
from apps.accounts.views.admin.scientific_groups import AdminScientificGroupListView
from apps.accounts.views.admin.scientific_group_create import AdminScientificGroupCreateView
from apps.accounts.views.admin.scientific_group_delete import AdminScientificGroupDeleteView
from apps.accounts.views.admin.scientific_group_assign import AdminScientificGroupAssignView
from apps.accounts.views.admin.user_directory import UserDirectoryView
from apps.accounts.views.admin.user_delete import UserDeleteView
from apps.accounts.views.admin.user_change_role import UserChangeRoleView
from apps.accounts.views.admin.user_replace_role import UserReplaceRoleView
from apps.accounts.views.admin.assessments import AdminAssessmentListView
from apps.accounts.views.admin.assessment_delete import AdminAssessmentDeleteView
from apps.accounts.views.admin.payment_management import AdminPaymentManagementView
from apps.accounts.views.admin.assessment_payments import AdminAssessmentPaymentsView



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
    path(
        "assessments/create/",
        AssessmentCreateView.as_view(),
        name="admin-assessment-create",
    ),
    path(
        "assessments/<uuid:assessment_id>/rules/",
        AssessmentRuleCreateView.as_view(),
        name="admin-assessment-rule-create",
    ),
    path(
        "payments/<uuid:payment_id>/review/",
        PaymentReviewView.as_view(),
        name="admin-payment-review",
    ),
    path("scientific-groups/", AdminScientificGroupListView.as_view(), name="admin-scientific-groups"),
    path("scientific-groups/create/", AdminScientificGroupCreateView.as_view(), name="admin-scientific-group-create"),
    path("scientific-groups/<uuid:group_id>/delete/", AdminScientificGroupDeleteView.as_view(), name="admin-scientific-group-delete"),
    path("scientific-groups/<uuid:group_id>/assign/", AdminScientificGroupAssignView.as_view(), name="admin-scientific-group-assign"),
    path("users/", UserDirectoryView.as_view(), name="admin-user-directory"),
    path("users/<int:user_id>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("users/<int:user_id>/change-role/", UserChangeRoleView.as_view(), name="user-change-role"),
    path("users/<int:user_id>/replace-role/", UserReplaceRoleView.as_view(), name="user-replace-role"),
    path("assessments/", AdminAssessmentListView.as_view(), name="admin-assessments"),
    path("assessments/<uuid:assessment_id>/delete/", AdminAssessmentDeleteView.as_view(), name="admin-assessment-delete"),
    path("payments/", AdminPaymentManagementView.as_view(), name="admin-payment-management"),
    path("payments/assessment/<uuid:assessment_id>/", AdminAssessmentPaymentsView.as_view(), name="admin-assessment-payments"),


]

