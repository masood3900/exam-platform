from django.views.generic import DetailView

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import Course


class AdminCourseDetailView(
    AdminRequiredMixin,
    DetailView,
):

    model = Course

    template_name = (
        "dashboard/admin/courses/detail.html"
    )

    context_object_name = "course"

    def get_queryset(self):

        return (
            Course.objects
            .select_related(
                "learning_path",
                "parent",
            )
            .prefetch_related(
                "prerequisites",
            )
        )
