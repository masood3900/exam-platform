from django.urls import reverse_lazy
from django.views.generic import UpdateView

from apps.accounts.forms.course import CourseForm
from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import Course


class AdminCourseUpdateView(
    AdminRequiredMixin,
    UpdateView,
):

    model = Course

    form_class = CourseForm

    template_name = (
        "dashboard/admin/courses/form.html"
    )

    context_object_name = "course"

    success_url = reverse_lazy(
        "accounts:admin-courses",
    )
