from django.urls import path
from apps.accounts.views.scientific_manager.bulk_review import BulkReviewView

from apps.accounts.views.admin.assessment_create import AssessmentCreateView
from apps.accounts.views.admin.assessment_rule_create import AssessmentRuleCreateView
from apps.accounts.views.scientific_manager.dashboard import (
    ScientificManagerDashboardView,
)
from apps.accounts.views.scientific_manager.objectives_api import ObjectivesAPIView
from apps.accounts.views.scientific_manager.course_students import CourseStudentsView
from apps.accounts.views.scientific_manager.student_detail import StudentDetailView
from apps.accounts.views.scientific_manager.attempt_detail import AttemptDetailView
from apps.accounts.views.scientific_manager.question_review import (
    QuestionReviewView,
)
from apps.accounts.views.scientific_manager.question_status_change import (
    QuestionStatusChangeView,
)
from apps.accounts.views.scientific_manager.assign_designer import AssignDesignerView
from apps.accounts.views.scientific_manager.remove_designer import RemoveDesignerView
from apps.accounts.views.scientific_manager.objective_create import ObjectiveCreateView
from apps.accounts.views.scientific_manager.topic_create import TopicCreateView
from apps.accounts.views.scientific_manager.user_directory import ScientificManagerUserDirectoryView
from apps.accounts.views.scientific_manager.assessment_delete import AssessmentDeleteView
from apps.accounts.views.scientific_manager.topic_delete import TopicDeleteView
from apps.accounts.views.scientific_manager.assessment_add_student import AssessmentAddStudentView
from apps.accounts.views.scientific_manager.assessment_toggle import AssessmentToggleActiveView
from apps.accounts.views.scientific_manager.assessment_pricing import AssessmentPricingView

app_name = "scientific_manager"

urlpatterns = [
    path(
        "dashboard/",
        ScientificManagerDashboardView.as_view(),
        name="dashboard",
    ),
    path(
        "assessments/create/",
        AssessmentCreateView.as_view(),
        name="scientific-manager-assessment-create",
    ),
    path(
        "assessments/<uuid:assessment_id>/rules/",
        AssessmentRuleCreateView.as_view(),
        name="scientific-manager-assessment-rule-create",
    ),
    path(
        "api/objectives/<uuid:topic_id>/",
        ObjectivesAPIView.as_view(),
        name="objectives-api",
    ),
    path(
        "question/<uuid:question_id>/review/",
        QuestionReviewView.as_view(),
        name="question-review",
    ),
    path(
        "question/<uuid:question_id>/status-change/",
        QuestionStatusChangeView.as_view(),
        name="question-status-change",
    ),
    path("assign-designer/", AssignDesignerView.as_view(), name="assign-designer"),
    path("remove-designer/<uuid:membership_id>/", RemoveDesignerView.as_view(), name="remove-designer"),
    path("question/bulk-review/", BulkReviewView.as_view(), name="bulk-review"),
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),
    path("objectives/create/", ObjectiveCreateView.as_view(), name="objective-create"),
    path("users/", ScientificManagerUserDirectoryView.as_view(), name="user-directory"),
    path("course/<uuid:group_id>/students/", CourseStudentsView.as_view(), name="course-students"),
    path("student/<int:student_id>/detail/", StudentDetailView.as_view(), name="student-detail"),
    path("attempt/<uuid:attempt_id>/detail/", AttemptDetailView.as_view(), name="attempt-detail"),
    path("assessments/<uuid:assessment_id>/delete/", AssessmentDeleteView.as_view(), name="assessment-delete"),
    path("topics/<uuid:topic_id>/delete/", TopicDeleteView.as_view(), name="topic-delete"),
    path("assessments/<uuid:assessment_id>/add-student/", AssessmentAddStudentView.as_view(), name="assessment-add-student"),
    path("assessments/<uuid:assessment_id>/toggle/", AssessmentToggleActiveView.as_view(), name="assessment-toggle"),
    path("assessments/<uuid:assessment_id>/pricing/", AssessmentPricingView.as_view(), name="assessment-pricing"),
]