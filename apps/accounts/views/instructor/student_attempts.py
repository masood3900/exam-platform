from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.accounts.models import User
from apps.accounts.services.instructor_dashboard_service import (
    InstructorDashboardService,
)


class InstructorStudentAttemptsView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = (
        "dashboard/instructor_student_attempts.html"
    )

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        student = get_object_or_404(
            User,
            id=kwargs["pk"],
            groups__name="Students",
            is_active=True,
        )

        context["student"] = student

        context["attempts"] = (
            InstructorDashboardService.student_attempts(
                student
            )
        )

        return context