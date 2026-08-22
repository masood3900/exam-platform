from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import Course


class AdminCourseToggleActiveView(
    AdminRequiredMixin,
    View,
):

    def post(
        self,
        request,
        pk,
    ):

        course = get_object_or_404(
            Course,
            pk=pk,
        )

        course.is_active = not course.is_active

        course.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return redirect(
            "accounts:admin-course-detail",
            pk=course.pk,
        )
