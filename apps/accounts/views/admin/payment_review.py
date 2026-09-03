from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.utils import timezone

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import PaymentRequest
from apps.assessments.services.assessment_enrollment_service import AssessmentEnrollmentService


class PaymentReviewView(AdminRequiredMixin, View):
    """تایید یا رد درخواست پرداخت"""

    def post(self, request, payment_id):
        payment = get_object_or_404(PaymentRequest, id=payment_id)
        action = request.POST.get("action")
        admin_note = request.POST.get("admin_note", "")
        
        if action == "approve":
            payment.status = PaymentRequest.Status.APPROVED
            payment.admin_note = admin_note
            payment.reviewed_at = timezone.now()
            payment.save()
            
            # فعال‌سازی آزمون
            if payment.assessment:
                AssessmentEnrollmentService.activate_paid_assessment(
                    student=payment.user,
                    assessment=payment.assessment,
                )
            
            messages.success(request, "درخواست تایید و فعال‌سازی شد.")
        
        elif action == "reject":
            payment.status = PaymentRequest.Status.REJECTED
            payment.admin_note = admin_note
            payment.reviewed_at = timezone.now()
            payment.save()
            
            messages.warning(request, "درخواست رد شد.")
        
        return redirect("accounts:admin-dashboard")