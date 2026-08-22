from django.views.generic import ListView

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import Course


class AdminCourseListView(
    AdminRequiredMixin,
    ListView,
):

    model = Course

    template_name = (
        "dashboard/admin/courses/list.html"
    )

    context_object_name = "courses"

    paginate_by = 25

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
            .order_by(
                "learning_path__order",
                "learning_path__name",
                "parent__name",
                "order",
                "name",
            )
        )