from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from apps.education.models import InstructorAssignment
from apps.assessments.models import (
    LearningPath,
    Assessment,
)


class LearningPathDetailView(
    LoginRequiredMixin,
    DetailView,
):

    model = LearningPath

    template_name = (
        "dashboard/path_detail.html"
    )

    context_object_name = (
        "learning_path"
    )

    def get_queryset(self):

        return (
            LearningPath.objects
            .filter(
                courses__enrollments__user=self.request.user,
                courses__enrollments__status="active",
            )
            .distinct()
        )

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        context["courses"] = (
            self.object.courses
            .filter(
                is_active=True,
                enrollments__user=self.request.user,
                enrollments__status="active",
            )
            .distinct()
        )

        context["assessments"] = (
            Assessment.objects
            .filter(
                course__learning_path=self.object,
                course__enrollments__user=self.request.user,
                course__enrollments__status="active",
                is_active=True,
            )
            .select_related(
                "course",
            )
            .distinct()
            .order_by(
                "assessment_type",
                "title",
            )
        )

        context["instructor_assignments"] = (
            InstructorAssignment.objects
            .filter(
                student=self.request.user,
                learning_path=self.object,
                is_active=True,
            )
            .select_related(
                "instructor",
            )
            .order_by(
                "instructor__first_name",
                "instructor__last_name",
            )
        )

        return context