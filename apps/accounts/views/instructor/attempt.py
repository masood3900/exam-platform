from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from apps.accounts.mixins import InstructorRequiredMixin
from apps.assessments.models import Attempt
from apps.accounts.services.instructor_dashboard_service import (
    InstructorDashboardService,
)


class InstructorAttemptDetailView(
    InstructorRequiredMixin,
    TemplateView,
):

    template_name = (
        "dashboard/instructor_attempt_detail.html"
    )

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        attempt = get_object_or_404(
            Attempt,
            id=kwargs["pk"],
            status=Attempt.Status.GRADED,
        )

        context["data"] = (
            InstructorDashboardService.attempt_detail(
                attempt
            )
        )

        return context