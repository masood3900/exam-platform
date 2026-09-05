from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.assessments.models import Question


class QuestionPreviewView(LoginRequiredMixin, TemplateView):
    """پیش‌نمایش سوال به صورت مشابه آزمون"""

    template_name = "dashboard/question_designer/question_preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question = get_object_or_404(
            Question.objects.prefetch_related("choices"),
            id=self.kwargs["question_id"],
        )

        context["question"] = question
        context["choices"] = question.choices.all()

        return context
