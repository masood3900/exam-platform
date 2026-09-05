from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.assessments.forms.payment_request_form import PaymentRequestForm
from apps.assessments.models import Assessment, PaymentAccount, PaymentRequest
from apps.assessments.services.discount_service import DiscountService


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

        # بازیابی اطلاعات تخفیف از session
        discount_info = request.session.get("discount_info")

        if discount_info and discount_info.get("assessment_id") == str(assessment.id):
            amount = discount_info.get("final_price", assessment.final_price)
        else:
            amount = assessment.final_price
            discount_info = None

        return render(request, self.template_name, {
            "form": form,
            "assessment": assessment,
            "amount": amount,
            "accounts": accounts,
            "discount_info": discount_info,
        })

    def post(self, request, assessment_id=None):
        assessment = get_object_or_404(Assessment, id=assessment_id)

        form = PaymentRequestForm(request.POST, request.FILES)

        if form.is_valid():
            payment_request = form.save(commit=False)
            payment_request.user = request.user
            payment_request.assessment = assessment

            # بازیابی اطلاعات تخفیف از session
            discount_info = request.session.get("discount_info")

            if discount_info and discount_info.get("assessment_id") == str(assessment.id):
                code_str = discount_info.get("code")

                try:
                    # ثبت نهایی استفاده از کد
                    result = DiscountService.confirm_discount_usage(
                        code_str=code_str,
                        assessment=assessment,
                        user=request.user,
                    )
                    payment_request.amount = result["final_price"]
                    messages.success(request, "کد تخفیف ثبت و درخواست پرداخت ارسال شد.")
                except ValueError as exc:
                    messages.error(request, f"کد تخفیف دیگر معتبر نیست: {exc}")
                    payment_request.amount = assessment.final_price
            else:
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
