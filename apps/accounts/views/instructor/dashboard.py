from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.accounts.mixins import InstructorRequiredMixin
from apps.accounts.services.instructor_dashboard_service import (
    InstructorDashboardService,
)


class InstructorDashboardView(
    InstructorRequiredMixin,
    TemplateView,
):

    template_name = (
        "dashboard/instructor.html"
    )

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        context["stats"] = (
            InstructorDashboardService.overall_stats()
        )
        context["recent_assessments"] = (
            InstructorDashboardService.recent_assessments()
        )
        context["students"] = (
            InstructorDashboardService.students()
        )


        return context