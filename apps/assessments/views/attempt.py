from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.assessments.models import Attempt


class QuestionNavigateView(
    LoginRequiredMixin,
    View,
):
    """
    جابه‌جایی بین سوالات آزمون
    """

    def get(
        self,
        request,
        attempt_id,
        number,
    ):

        attempt = get_object_or_404(
            Attempt,
            id=attempt_id,
            student=request.user,
        )

        if number < 1:
            number = 1

        if number > attempt.total_questions:
            return redirect(
                "assessments:result",
                attempt_id=attempt.id,
            )

        return redirect(
            "assessments:question",
            attempt_id=attempt.id,
            number=number,
        )