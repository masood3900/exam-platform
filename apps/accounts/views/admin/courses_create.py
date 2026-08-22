from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.accounts.mixins import AdminRequiredMixin
from apps.accounts.forms import CourseForm
from apps.assessments.models import Course


class AdminCourseCreateView(
    AdminRequiredMixin,
    CreateView,
):

    model = Course
    form_class = CourseForm

    template_name = (
        "dashboard/admin/courses/form.html"
    )

    success_url = reverse_lazy(
        "accounts:admin-courses"
    )


