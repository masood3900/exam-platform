from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.assessments.forms.discount_code_form import DiscountCodeForm
from apps.assessments.models import Assessment
from apps.assessments.services.discount_service import DiscountService


class ApplyDiscountView(LoginRequiredMixin, View):
    """اعمال کد تخفیف روی آزمون (فقط محاسبه)"""

    def post(self, request, assessment_id):
        assessment = get_object_or_404(
            Assessment,
            id=assessment_id,
            is_active=True,
        )

        form = DiscountCodeForm(request.POST)

        if form.is_valid():
            code_str = form.cleaned_data["code"]

            try:
                # فقط محاسبه تخفیف بدون ثبت استفاده
                result = DiscountService.calculate_discount(
                    code_str=code_str,
                    assessment=assessment,
                    user=request.user,
                )

                # ذخیره اطلاعات در session برای استفاده در پرداخت
                request.session["discount_info"] = {
                    "assessment_id": str(assessment.id),
                    "code": code_str,
                    "original_price": result["original_price"],
                    "discount_percent": result["discount_percent"],
                    "final_price": result["final_price"],
                    "code_discount": result["code_discount"],
                    "base_discount": result["base_discount"],
                }

                messages.success(
                    request,
                    f"کد تخفیف اعمال شد! "
                    f"تخفیف: {result['code_discount']}٪ + "
                    f"تخفیف پایه: {result['base_discount']}٪ = "
                    f"مجموع: {result['discount_percent']}٪\n"
                    f"قیمت نهایی: {result['final_price']:,} تومان\n"
                    f"⚠️ در صورت عدم ارسال درخواست، کد مصرف نمی‌شود.",
                )

            except ValueError as exc:
                messages.error(request, str(exc))

        else:
            messages.error(request, "لطفاً کد تخفیف را وارد کنید.")

        return redirect(
            "accounts:payment-request-assessment",
            assessment_id=assessment.id,
        )
