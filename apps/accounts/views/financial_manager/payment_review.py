from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.assessments.models import PaymentRequest
from apps.assessments.services.assessment_enrollment_service import AssessmentEnrollmentService


class FinancialPaymentReviewView(LoginRequiredMixin, View):
    """تایید یا رد پرداخت توسط مدیر مالی"""

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
            
            # فعال‌سازی دوره
            if payment.course:
                from apps.assessments.services.enrollment_service import EnrollmentService
                from apps.assessments.models import CourseEnrollment
                
                enrollment, created = CourseEnrollment.objects.get_or_create(
                    user=payment.user,
                    course=payment.course,
                )
                enrollment.status = CourseEnrollment.Status.ACTIVE
                enrollment.payment_status = CourseEnrollment.PaymentStatus.PAID
                enrollment.activated_at = timezone.now()
                enrollment.save()
            
            messages.success(request, "پرداخت تایید و فعال‌سازی شد.")
        
        elif action == "reject":
            payment.status = PaymentRequest.Status.REJECTED
            payment.admin_note = admin_note
            payment.reviewed_at = timezone.now()
            payment.save()
            messages.warning(request, "پرداخت رد شد.")
        
        return redirect("accounts:financial_manager:dashboard")