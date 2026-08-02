from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.assessments.models import Attempt


class QuestionDetailView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = "assessments/question/detail.html"

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):

        self.attempt = get_object_or_404(
            Attempt.objects.select_related(
                "assessment",
                "student",
            ),
            id=kwargs["attempt_id"],
            student=request.user,
        )

        self.question = (
            self.attempt.questions
            .prefetch_related("choices")
            .filter(
                order=kwargs["number"],
            )
            .prefetch_related(
                "choices",
            )
            .first()
        )

        if self.question is None:

            return redirect(
                "assessments:result",
                attempt_id=self.attempt.id,
            )

        return super().get(
            request,
            *args,
            **kwargs,
        )

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs,
        )

        context["attempt"] = self.attempt
        context["question"] = self.question
        context["choices"] = self.question.choices.all()
        context["question_number"] = self.question.order
        context["total_questions"] = self.attempt.total_questions

        return context