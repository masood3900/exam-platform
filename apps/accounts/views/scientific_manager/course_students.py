from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from apps.accounts.services.student_directory_service import StudentDirectoryService
from apps.assessments.models import ScientificGroup


class CourseStudentsView(LoginRequiredMixin, TemplateView):
    """لیست دانشجویان یک دوره"""

    template_name = "dashboard/scientific_manager/course_students.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.kwargs["group_id"]

        group = get_object_or_404(ScientificGroup, id=group_id)
        students = StudentDirectoryService.get_group_students_summary(group_id)

        context["group"] = group
        context["students"] = students
        return context
