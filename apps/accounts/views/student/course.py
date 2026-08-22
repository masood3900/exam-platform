from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from apps.assessments.models import (
    Course,
    CourseEnrollment,
)


class CourseDetailView(
    LoginRequiredMixin,
    DetailView,
):

    model = Course

    template_name = (
        "dashboard/course_detail.html"
    )

    context_object_name = "course"

    def get_queryset(self):

        return (
            Course.objects
            .filter(
                id=self.kwargs["pk"],
                learning_path_id=self.kwargs["path_pk"],
                enrollments__user=self.request.user,
                enrollments__status=(
                    CourseEnrollment.Status.ACTIVE
                ),
                is_active=True,
            )
            .select_related(
                "learning_path",
                "parent",
            )
            .prefetch_related(
                "categories",
            )
            .distinct()
        )