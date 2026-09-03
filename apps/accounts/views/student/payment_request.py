from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.assessments.forms.payment_request_form import PaymentRequestForm
from apps.assessments.models import Assessment, PaymentAccount, PaymentRequest


class PaymentRequestView(LoginRequiredMixin, View):
    """درخواست پرداخت برای فعال‌سازی"""

    template_name = "dashboard/student/payment_request.html"

    def get(self, request, assessment_id=None):
        assessment = get_object_or_404(Assessment, id=assessment_id)
        
        # چک درخواست در انتظار
        existing = PaymentRequest.objects.filter(
            user=request.user,
            assessment=assessment,
            status=PaymentRequest.Status.PENDING,
        ).first()
        
        if existing:
            messages.info(request, "شما یک درخواست در انتظار بررسی دارید.")
            return redirect("accounts:payment-status")
        
        # چک درخواست تایید شده
        approved = PaymentRequest.objects.filter(
            user=request.user,
            assessment=assessment,
            status=PaymentRequest.Status.APPROVED,
        ).exists()
        
        if approved:
            messages.info(request, "این آزمون قبلاً فعال شده است.")
            return redirect("accounts:dashboard")
        
        form = PaymentRequestForm()
        accounts = PaymentAccount.objects.filter(is_active=True)
        
        return render(request, self.template_name, {
            "form": form,
            "assessment": assessment,
            "amount": assessment.final_price,
            "accounts": accounts,
        })

    def post(self, request, assessment_id=None):
        assessment = get_object_or_404(Assessment, id=assessment_id)
        
        form = PaymentRequestForm(request.POST, request.FILES)
        
        if form.is_valid():
            payment_request = form.save(commit=False)
            payment_request.user = request.user
            payment_request.assessment = assessment
            payment_request.amount = assessment.final_price
            payment_request.save()
            
            messages.success(request, "درخواست پرداخت ثبت شد.")
            return redirect("accounts:payment-status")
        
        accounts = PaymentAccount.objects.filter(is_active=True)
        
        return render(request, self.template_name, {
            "form": form,
            "assessment": assessment,
            "amount": assessment.final_price,
            "accounts": accounts,
        })
