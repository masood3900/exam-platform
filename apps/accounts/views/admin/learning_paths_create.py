from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.accounts.forms import LearningPathForm
from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import LearningPath


class AdminLearningPathCreateView(
    AdminRequiredMixin,
    CreateView,
):

    model = LearningPath

    form_class = LearningPathForm

    template_name = (
        "dashboard/admin/learning_path_form.html"
    )

    success_url = reverse_lazy(
        "accounts:admin-learning-paths"
    )