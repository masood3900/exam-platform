from django.views.generic import ListView

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import LearningPath


class AdminLearningPathListView(
    AdminRequiredMixin,
    ListView,
):

    model = LearningPath

    template_name = (
        "dashboard/admin/learning_paths/list.html"
    )

    context_object_name = "learning_paths"

    paginate_by = 25

    def get_queryset(self):

        return (
            LearningPath.objects
            .prefetch_related(
                "prerequisites",
            )
            .order_by(
                "order",
                "name",
            )
        )