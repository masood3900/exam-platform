from django.urls import reverse
from django.views.generic import UpdateView

from apps.accounts.forms.learning_path import (
    LearningPathForm,
)
from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import LearningPath


class AdminLearningPathUpdateView(
    AdminRequiredMixin,
    UpdateView,
):

    model = LearningPath

    form_class = LearningPathForm

    template_name = (
        "dashboard/admin/learning_path_form.html"
    )

    context_object_name = "learning_path"

    def get_success_url(self):

        return reverse(
            "accounts:admin-learning-path-detail",
            kwargs={
                "pk": self.object.pk,
            },
        )
