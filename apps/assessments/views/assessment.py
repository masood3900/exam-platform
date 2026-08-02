from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.assessments.models import Assessment
from apps.assessments.services.attempt_service import AttemptService


class AssessmentStartView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        assessment_id,
    ):

        assessment = get_object_or_404(
            Assessment,
            id=assessment_id,
            is_active=True,
        )

        attempt = AttemptService.start_attempt(
            student=request.user,
            assessment=assessment,
        )

        return redirect(
            "assessments:question",
            attempt_id=attempt.id,
            number=1,
        )