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
        if self.attempt.status != Attempt.Status.STARTED:
            return redirect(
                "assessments:result",
                attempt_id=self.attempt.id,
            )


        self.attempt_question = (
            self.attempt.questions
            .prefetch_related(
                "choices__original_choice",
            )
            .filter(
                order=kwargs["number"],
            )
            .first()
        )


        if self.attempt_question is None:

            return redirect(
                "assessments:result",
                attempt_id=self.attempt.id,
            )
        self.selected_choice_ids = set(
            self.attempt_question.choices.filter(
                selected=True,
            ).values_list(
                "id",
                flat=True,
            )
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

        context["question"] = (
            self.attempt_question.question
        )

        context["attempt_question"] = (
            self.attempt_question
        )

        context["choices"] = (
            self.attempt_question.choices.all()
        )

        context["question_number"] = (
            self.attempt_question.order
        )

        context["total_questions"] = (
            self.attempt.total_questions
        )
        context["selected_choice_ids"] = (
            self.selected_choice_ids
        )

        return context