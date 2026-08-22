from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.assessments.models import Attempt, AttemptQuestion
from apps.assessments.services import AttemptService
from django.contrib.auth.mixins import LoginRequiredMixin

class AnswerView(LoginRequiredMixin,View):

    def post(
        self,
        request,
        attempt_id,
    ):

        attempt = get_object_or_404(
            Attempt,
            id=attempt_id,
            student=request.user,
        )
        question_number = int(request.POST.get("question_number"))
   
        print(request.POST)
        attempt_question = get_object_or_404(
            AttemptQuestion,
            attempt=attempt,
            order=question_number,
        )

        choice_id = request.POST.get(
            "choice"
        )

        # اگر گزینه‌ای انتخاب نشده باشد
        if not choice_id:
            return redirect(
                "assessments:question",
                attempt_id= attempt.id,
                number= question_number,
            )
        # ثبت پاسخ
        selected_choice_ids = [
            choice_id
        ]
        AttemptService.submit_answer(
            attempt=attempt,
            attempt_question=attempt_question,
            selected_choice_ids=selected_choice_ids,
        )
        
        AttemptService.check_answer(
            attempt=attempt,
            attempt_question=attempt_question,
            
        )

        next_number = int(question_number)+1
        # اگر آزمون تمام شده باشد

        if next_number > attempt.total_questions:
            AttemptService.finish_attempt(
                attempt,
            )
            return redirect(
                "assessments:result",
                attempt_id= attempt.id,

            )
        # سؤال بعد
        return redirect(
            "assessments:question",
            attempt_id=attempt.id,
            number=next_number,
        )