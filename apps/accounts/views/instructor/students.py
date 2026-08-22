from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from apps.accounts.mixins import InstructorRequiredMixin
from apps.accounts.models import User
from apps.accounts.services.instructor_dashboard_service import (
    InstructorDashboardService,
)


class InstructorStudentListView(
    InstructorRequiredMixin,
    TemplateView,
):

    template_name = (
        "dashboard/instructor_students.html"
    )

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        context["students"] = (
            InstructorDashboardService.students(
                limit=None
            )
        )

        return context


class InstructorStudentDetailView(
    InstructorRequiredMixin,
    TemplateView,
):

    template_name = (
        "dashboard/instructor_student_detail.html"
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

        context["data"] = (
            InstructorDashboardService.student_detail(
                student=student,
                instructor=self.request.user,
            )
        )

        return context