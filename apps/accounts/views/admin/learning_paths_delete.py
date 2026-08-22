from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import LearningPath


class AdminLearningPathDeleteView(
    AdminRequiredMixin,
    DeleteView,
):

    model = LearningPath

    template_name = (
        "dashboard/admin/learning_path_confirm_delete.html"
    )

    context_object_name = "learning_path"

    success_url = reverse_lazy(
        "accounts:admin-learning-paths"
    )

    def form_valid(self, form):

        messages.success(
            self.request,
            "مسیر آموزشی با موفقیت حذف شد.",
        )

        return super().form_valid(form)