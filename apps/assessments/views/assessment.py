from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from apps.assessments.models import Assessment
from apps.assessments.services.attempt_service import AttemptService
from apps.assessments.services.assessment_enrollment_service import AssessmentEnrollmentService

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

        # چک کن پرداخت شده
        from apps.assessments.models import AssessmentEnrollment
        paid_enrollment = AssessmentEnrollment.objects.filter(
            user=request.user,
            assessment=assessment,
            payment_status="paid",
        ).first()
        
        # اگه پرداخت نشده، enroll کن
        if not paid_enrollment:
            AssessmentEnrollmentService.enroll(
                student=request.user,
                assessment=assessment,
            )

        try:

            attempt = AttemptService.start_attempt(
                student=request.user,
                assessment=assessment,
            )

        except ValueError as e:

            messages.error(
                request,
                str(e)
            )

            return redirect(
                "accounts:dashboard"
            )


        return redirect(
            "assessments:question",
            attempt_id=attempt.id,
            number=1,
        )