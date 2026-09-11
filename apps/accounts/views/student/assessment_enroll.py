from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.assessments.models import Assessment
from apps.assessments.services.assessment_enrollment_service import (
    AssessmentEnrollmentService,
)


class AssessmentEnrollView(LoginRequiredMixin, View):
    """ثبت‌نام در آزمون"""

    def post(self, request, assessment_id):
        assessment = get_object_or_404(
            Assessment,
            id=assessment_id,
            is_active=True,
        )

        try:
            enrollment = AssessmentEnrollmentService.enroll(
                student=request.user,
                assessment=assessment,
            )

        except ValueError as exc:
            messages.error(request, str(exc))
            return redirect("core:assessments")

        if enrollment.has_access:
            messages.success(
                request,
                f"✅ آزمون «{assessment.title}» به داشبورد شما اضافه شد. "
                f"می‌توانید از داشبورد شروع کنید.",
            )
        else:
            messages.info(
                request,
                f"📝 آزمون «{assessment.title}» به داشبورد شما اضافه شد. "
                f"شما {assessment.demo_attempts} بار آزمایشی رایگان دارید.",
            )

        # برگشت به صفحه جزئیات آزمون
        return redirect(
            "core:assessment-detail",
            assessment_id=assessment.id,
        )
