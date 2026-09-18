from django.conf import settings
from django.core.exceptions import PermissionDenied
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
from apps.accounts.views.question_designer.image_upload import ImageUploadView


app_name = "question_designer"


class QuestionDesignerGuardMixin:
    """
    Mixin که چک می‌کنه آیا بخش طراح سوال فعاله یا نه.
    توی main: ENABLE_QUESTION_DESIGNER=False → 403
    توی stage: ENABLE_QUESTION_DESIGNER=True → دسترسی باز
    """

    def dispatch(self, request, *args, **kwargs):
        if not getattr(settings, "ENABLE_QUESTION_DESIGNER", False):
            raise PermissionDenied(
                "بخش طراحی سوال در این محیط غیرفعال است."
            )
        return super().dispatch(request, *args, **kwargs)


def guarded(view_class):
    """اعمال guard روی همه ویوها"""
    return type(
        f"Guarded{view_class.__name__}",
        (QuestionDesignerGuardMixin, view_class),
        {"__module__": view_class.__module__},
    )


urlpatterns = [
    path(
        "dashboard/",
        guarded(QuestionDesignerDashboardView).as_view(),
        name="dashboard",
    ),
    path(
        "question/<uuid:question_id>/detail/",
        guarded(QuestionDetailAPIView).as_view(),
        name="question-detail",
    ),
    path(
        "question/create/",
        guarded(QuestionCreateView).as_view(),
        name="question-create",
    ),
    path(
        "question/<uuid:question_id>/submit/",
        guarded(QuestionSubmitView).as_view(),
        name="question-submit",
    ),
    path(
        "api/courses/<uuid:group_id>/",
        guarded(CoursesAPIView).as_view(),
        name="courses-api",
    ),
    path(
        "api/learning-objectives/<uuid:course_id>/",
        guarded(LearningObjectivesAPIView).as_view(),
        name="learning-objectives-api",
    ),
    path(
        "question/bulk-submit/",
        guarded(BulkSubmitView).as_view(),
        name="bulk-submit",
    ),
    path(
        "question/<uuid:question_id>/edit/",
        guarded(QuestionEditView).as_view(),
        name="question-edit",
    ),
    path(
        "question/<uuid:question_id>/delete/",
        guarded(QuestionDeleteView).as_view(),
        name="question-delete",
    ),
    path(
        "question/<uuid:question_id>/preview/",
        guarded(QuestionPreviewView).as_view(),
        name="question-preview",
    ),
    path(
        "upload-image/",
        guarded(ImageUploadView).as_view(),
        name="image-upload",
    ),
]
