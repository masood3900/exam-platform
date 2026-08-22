from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.assessments.models import Attempt


class AssessmentStartView(LoginRequiredMixin, View):

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
            number = attempt.total_questions

        return redirect(
            "assessments:question",
            attempt_id=attempt.id,
            number=number,
        )