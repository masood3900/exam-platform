from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from apps.assessments.models import LearningObjective


class LearningObjectiveDetailView(
    LoginRequiredMixin,
    DetailView,
):

    model = LearningObjective

    template_name = (
        "dashboard/learning_objective_detail.html"
    )

    context_object_name = "objective"

    def get_queryset(self):

        category_pk = self.kwargs["category_pk"]

        return (
            LearningObjective.objects
            .filter(
                id=self.kwargs["pk"],
                category_id=category_pk,

                category__course__enrollments__user=self.request.user,
                category__course__enrollments__status="active",

                is_active=True,
            )
            .select_related(
                "category",
                "category__course",
                "category__course__learning_path",
            )
            .prefetch_related(
                "questions",
            )
            .distinct()
        )