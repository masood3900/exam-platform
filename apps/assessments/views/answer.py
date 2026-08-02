from django.shortcuts import redirect
from django.views import View
from django.shortcuts import get_object_or_404

from apps.assessments.models import Attempt, AttemptQuestion
from apps.assessments.services import AttemptService


class AnswerView(View):

    def post(self, request, attempt_id):

        attempt = get_object_or_404(
            Attempt,
            id=attempt_id
        )

        question_number = request.POST.get(
            "question_number"
        )

        attempt_question = get_object_or_404(
            AttemptQuestion,
            attempt=attempt,
            order=question_number,
        )

        choice_id = request.POST.get(
            "choice"
        )


        AttemptService.submit_answer(
            attempt_question=attempt_question,
            choice_id=choice_id,
        )


        return redirect(
            "assessments:question",
            attempt_id=attempt.id,
            number=int(question_number) + 1,
        )