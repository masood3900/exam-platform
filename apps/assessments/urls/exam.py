from django.urls import path

from apps.assessments.views.assessment import AssessmentStartView
from apps.assessments.views.question import QuestionDetailView
from apps.assessments.views.answer import AnswerView

app_name = "assessments"


urlpatterns = [

    path(
        "<uuid:assessment_id>/start/",
        AssessmentStartView.as_view(),
        name="start",
    ),

    path(
        "attempt/<uuid:attempt_id>/question/<int:number>/",
        QuestionDetailView.as_view(),
        name="question",
    ),
    path(
        "attempt/<uuid:attempt_id>/answer/",
        AnswerView.as_view(),
        name="answer",
    ),
    

]