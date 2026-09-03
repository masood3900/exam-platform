from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.accounts.mixins import InstructorRequiredMixin
from apps.accounts.services.instructor_dashboard_service import (
    InstructorDashboardService,
)
from apps.assessments.models import (
    CourseInstructorAssignment,
    Lesson,
    Exercise,
    Assessment,
)


class InstructorDashboardView(
    InstructorRequiredMixin,
    TemplateView,
):

    template_name = "dashboard/instructor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        instructor = self.request.user

        context["stats"] = (
            InstructorDashboardService.overall_stats(instructor)
        )
        context["recent_assessments"] = (
            InstructorDashboardService.recent_assessments(instructor)
        )
        context["students"] = (
            InstructorDashboardService.students(instructor)
        )
        
        # دوره‌های تخصیص داده شده
        context["assigned_courses"] = (
            CourseInstructorAssignment.objects.filter(
                instructor=instructor,
                is_active=True,
            ).select_related("course")
        )
        
        # درس‌های این مدرس
        instructor_course_ids = CourseInstructorAssignment.objects.filter(
            instructor=instructor,
            is_active=True,
        ).values_list("course_id", flat=True)
        
        context["my_lessons"] = Lesson.objects.filter(
            course_id__in=instructor_course_ids,
            is_active=True,
        ).select_related("course").order_by("-created_at")
        
        # تمرین‌های این مدرس
        context["my_exercises"] = Exercise.objects.filter(
            lesson__course_id__in=instructor_course_ids,
            is_active=True,
        ).select_related("lesson", "lesson__course").order_by("-created_at")

        return context