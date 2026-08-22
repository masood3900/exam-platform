from django.views.generic import DetailView

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import LearningPath


class AdminLearningPathDetailView(
    AdminRequiredMixin,
    DetailView,
):

    model = LearningPath

    template_name = (
        "dashboard/admin/learning_paths/detail.html"
    )

    context_object_name = "learning_path"

    def get_queryset(self):

        return (
            LearningPath.objects
            .prefetch_related(
                "prerequisites",
                "courses",
            )
            .order_by(
                "order",
                "name",
            )
        )
