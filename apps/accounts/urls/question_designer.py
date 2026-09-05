from django.urls import path

from apps.accounts.views.question_designer.dashboard import (
    QuestionDesignerDashboardView,
)
from apps.accounts.views.question_designer.question_detail import (
    QuestionDetailAPIView,
)
from apps.accounts.views.question_designer.question_create import (
    QuestionCreateView,
)
from apps.accounts.views.question_designer.question_submit import (
    QuestionSubmitView,
)
from apps.accounts.views.question_designer.courses_api import (
    CoursesAPIView,
)
from apps.accounts.views.question_designer.learning_objectives_api import (
    LearningObjectivesAPIView,
)
from apps.accounts.views.question_designer.bulk_submit import BulkSubmitView
from apps.accounts.views.question_designer.question_edit import QuestionEditView
from apps.accounts.views.question_designer.question_delete import QuestionDeleteView
from apps.accounts.views.question_designer.question_preview import QuestionPreviewView


app_name = "question_designer"

urlpatterns = [
    path(
        "dashboard/",
        QuestionDesignerDashboardView.as_view(),
        name="dashboard",
    ),
    path(
        "question/<uuid:question_id>/detail/",
        QuestionDetailAPIView.as_view(),
        name="question-detail",
    ),
    path(
        "question/create/",
        QuestionCreateView.as_view(),
        name="question-create",
    ),
    path(
        "question/<uuid:question_id>/submit/",
        QuestionSubmitView.as_view(),
        name="question-submit",
    ),
    path(
        "api/courses/<uuid:group_id>/",
        CoursesAPIView.as_view(),
        name="courses-api",
    ),
    path(
        "api/learning-objectives/<uuid:course_id>/",
        LearningObjectivesAPIView.as_view(),
        name="learning-objectives-api",
    ),
    path("question/bulk-submit/", BulkSubmitView.as_view(), name="bulk-submit"),
    path("question/<uuid:question_id>/edit/", QuestionEditView.as_view(), name="question-edit"),
    path("question/<uuid:question_id>/delete/", QuestionDeleteView.as_view(), name="question-delete"),
    path("question/<uuid:question_id>/preview/", QuestionPreviewView.as_view(), name="question-preview"),
]
