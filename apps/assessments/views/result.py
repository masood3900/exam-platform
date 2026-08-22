from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.assessments.models import Attempt
from apps.assessments.services.analytics_service import AnalyticsService
from apps.assessments.services.attempt_service import AttemptService


class ResultView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = (
        "assessments/result/detail.html"
    )


    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        attempt = get_object_or_404(
            Attempt.objects.select_related(
                "assessment",
                "student",
            ).prefetch_related(
                "questions__choices",
            ),
            id=kwargs["attempt_id"],
            student=self.request.user,
        )


        context["attempt"] = attempt

        context["can_retry"] = (
            AttemptService.can_start_attempt(
                student=self.request.user,
                assessment=attempt.assessment,
            )
        )



        context["questions"] = (
            attempt.questions.all()
        )


        context["objective_report"] = (
            AnalyticsService.learning_objective_report(
                attempt
            )
        )


        return context