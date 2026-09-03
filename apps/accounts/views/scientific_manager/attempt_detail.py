from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from apps.assessments.models import Attempt
from apps.assessments.services.analytics_service import AnalyticsService


class AttemptDetailView(LoginRequiredMixin, TemplateView):
    """نمایش نتیجه یک تلاش"""

    template_name = "dashboard/scientific_manager/attempt_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempt_id = self.kwargs["attempt_id"]

        attempt = get_object_or_404(
            Attempt.objects.select_related("assessment", "student"),
            id=attempt_id,
        )

        objective_report = []
        try:
            objective_report = AnalyticsService.learning_objective_report(attempt)
        except:
            pass

        questions = attempt.questions.select_related("question").order_by("order")

        context["attempt"] = attempt
        context["objective_report"] = objective_report
        context["questions"] = questions
        return context
