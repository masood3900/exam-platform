from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import Assessment, Attempt, AssessmentEnrollment, AssessmentRule, PaymentRequest


class AdminAssessmentDeleteView(AdminRequiredMixin, View):
    """حذف آزمون"""

    def post(self, request, assessment_id):
        assessment = get_object_or_404(Assessment, id=assessment_id)
        
        title = assessment.title
        
        # پاک کردن وابسته‌ها
        Attempt.objects.filter(assessment=assessment).delete()
        AssessmentEnrollment.objects.filter(assessment=assessment).delete()
        AssessmentRule.objects.filter(assessment=assessment).delete()
        PaymentRequest.objects.filter(assessment=assessment).delete()
        
        assessment.delete()
        
        messages.success(request, f"آزمون «{title}» حذف شد.")
        return redirect("accounts:admin-assessments")