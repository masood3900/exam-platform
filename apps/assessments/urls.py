from django.urls import path

from apps.assessments.views import (
    AssessmentStartView,
    QuestionNavigateView,
    QuestionDetailView,
    AnswerView,
    ResultView,
    AttemptHistoryView,
)
from apps.assessments.views.code_execute import (
    CodeExecuteView,
    CodeCheckView,
)
from apps.assessments.views.apply_discount import (
    ApplyDiscountView,
)


app_name = "assessments"


urlpatterns = [
    path(
        "attempts/history/",
        AttemptHistoryView.as_view(),
        name="attempt-history",
    ),

    # شروع آزمون
    path(
        "exam/assessment/<uuid:assessment_id>/start/",
        AssessmentStartView.as_view(),
        name="start",
    ),

    # نمایش سؤال
    path(
        "exam/attempt/<uuid:attempt_id>/question/<int:number>/",
        QuestionDetailView.as_view(),
        name="question",
    ),

    # حرکت بین سؤالات
    path(
        "exam/attempt/<uuid:attempt_id>/navigate/<int:number>/",
        QuestionNavigateView.as_view(),
        name="navigate",
    ),

    # ثبت پاسخ
    path(
        "exam/attempt/<uuid:attempt_id>/answer/",
        AnswerView.as_view(),
        name="answer",
    ),

    # نتیجه
    path(
        "exam/attempt/<uuid:attempt_id>/result/",
        ResultView.as_view(),
        name="result",
    ),
    path(
        "api/code/execute/",
        CodeExecuteView.as_view(),
        name="code-execute",
    ),
    path(
        "api/exercise/<uuid:exercise_id>/check/",
        CodeCheckView.as_view(),
        name="exercise-check",
    ),
    path(
        "assessment/<uuid:assessment_id>/apply-discount/",
        ApplyDiscountView.as_view(),
        name="apply-discount",
    ),
]
