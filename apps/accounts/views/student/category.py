from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from apps.assessments.models import QuestionCategory


class QuestionCategoryDetailView(
    LoginRequiredMixin,
    DetailView,
):

    model = QuestionCategory

    template_name = (
        "dashboard/category_detail.html"
    )

    context_object_name = "category"

    def get_queryset(self):

        course_pk = self.kwargs["course_pk"]

        return (
            QuestionCategory.objects
            .filter(
                id=self.kwargs["pk"],
                course_id=course_pk,

                course__enrollments__user=self.request.user,
                course__enrollments__status="active",

                is_active=True,
            )
            .select_related(
                "course",
                "course__learning_path",
                "parent",
            )
            .prefetch_related(
                "learning_objectives",
            )
            .distinct()
        )