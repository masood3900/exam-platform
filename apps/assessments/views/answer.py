from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta

from apps.assessments.models import Attempt, AttemptQuestion
from apps.assessments.services import AttemptService


class AnswerView(LoginRequiredMixin, View):

    def post(self, request, attempt_id):
        attempt = get_object_or_404(
            Attempt,
            id=attempt_id,
            student=request.user,
        )

        # چک زمان
        if attempt.started_at:
            end_time = attempt.started_at + timedelta(
                minutes=attempt.assessment.duration_minutes
            )
            if timezone.now() > end_time:
                # زمان تموم شده
                AttemptService.finish_attempt(attempt)
                return redirect("assessments:result", attempt_id=attempt.id)

        question_number = int(request.POST.get("question_number"))
        attempt_question = get_object_or_404(
            AttemptQuestion,
            attempt=attempt,
            order=question_number,
        )

        choice_id = request.POST.get("choice")

        # اگه گزینه‌ای انتخاب شده باشه، ثبت کن
        if choice_id:
            selected_choice_ids = [choice_id]
            AttemptService.submit_answer(
                attempt=attempt,
                attempt_question=attempt_question,
                selected_choice_ids=selected_choice_ids,
            )
            AttemptService.check_answer(
                attempt=attempt,
                attempt_question=attempt_question,
            )

        next_number = int(question_number) + 1

        # اگه آزمون تمام شده باشه
        if next_number > attempt.total_questions:
            AttemptService.finish_attempt(attempt)
            return redirect("assessments:result", attempt_id=attempt.id)

        # سوال بعدی
        return redirect(
            "assessments:question",
            attempt_id=attempt.id,
            number=next_number,
        )
