from django.db import transaction
from django.utils import timezone

from apps.assessments.models import (
    Assessment,
    DiscountCode,
    DiscountCodeUsage,
)


class DiscountService:
    """سرویس مدیریت کدهای تخفیف"""

    @staticmethod
    def validate_code(code_str, assessment, user):
        """
        بررسی اعتبار کد تخفیف برای کاربر و آزمون
        
        Args:
            code_str: رشته کد تخفیف
            assessment: آزمون مورد نظر
            user: کاربر
        
        Returns:
            DiscountCode: کد تخفیف معتبر
        
        Raises:
            ValueError: اگر کد نامعتبر باشد
        """
        try:
            code = DiscountCode.objects.get(
                code__iexact=code_str.strip(),
                is_active=True,
            )
        except DiscountCode.DoesNotExist:
            raise ValueError("کد تخفیف نامعتبر است.")

        # بررسی اعتبار زمانی
        if not code.is_valid:
            raise ValueError("کد تخفیف منقضی شده یا ظرفیت آن تکمیل است.")

        # بررسی اختصاص به آزمون
        if code.assessment and code.assessment != assessment:
            raise ValueError("این کد تخفیف برای این آزمون نیست.")

        # بررسی استفاده قبلی کاربر از این کد (بدون توجه به آزمون)
        already_used = DiscountCodeUsage.objects.filter(
            code=code,
            user=user,
        ).exists()

        if already_used:
            raise ValueError("شما قبلاً از این کد تخفیف استفاده کرده‌اید.")

        return code

    @staticmethod
    def calculate_discount(code_str, assessment, user):
        """
        محاسبه تخفیف بدون ثبت استفاده
        
        Returns:
            dict: شامل قیمت اصلی، درصد تخفیف، قیمت نهایی
        """
        code = DiscountService.validate_code(code_str, assessment, user)

        # محاسبه قیمت
        original_price = assessment.final_price

        if original_price == 0:
            raise ValueError("این آزمون رایگان است و نیاز به کد تخفیف ندارد.")

        # جمع درصد تخفیف پایه و کد
        total_discount = assessment.discount_percent + code.discount_percent

        # محدودیت تا ۱۰۰٪
        if total_discount > 100:
            total_discount = 100

        final_price = original_price * (100 - total_discount) // 100

        return {
            "original_price": original_price,
            "discount_percent": total_discount,
            "final_price": final_price,
            "code_discount": code.discount_percent,
            "base_discount": assessment.discount_percent,
        }

    @staticmethod
    @transaction.atomic
    def confirm_discount_usage(code_str, assessment, user):
        """
        ثبت نهایی استفاده از کد تخفیف (وقتی درخواست پرداخت ثبت می‌شود)
        
        Returns:
            dict: شامل قیمت اصلی، درصد تخفیف، قیمت نهایی
        """
        code = DiscountService.validate_code(code_str, assessment, user)

        # محاسبه قیمت
        original_price = assessment.final_price

        if original_price == 0:
            raise ValueError("این آزمون رایگان است و نیاز به کد تخفیف ندارد.")

        # جمع درصد تخفیف پایه و کد
        total_discount = assessment.discount_percent + code.discount_percent

        # محدودیت تا ۱۰۰٪
        if total_discount > 100:
            total_discount = 100

        final_price = original_price * (100 - total_discount) // 100

        # ثبت استفاده از کد
        DiscountCodeUsage.objects.create(
            code=code,
            user=user,
            assessment=assessment,
            discount_percent=code.discount_percent,
            original_price=original_price,
            discounted_price=final_price,
        )

        # افزایش شمارنده استفاده
        code.used_count += 1
        code.save(update_fields=["used_count"])

        return {
            "original_price": original_price,
            "discount_percent": total_discount,
            "final_price": final_price,
            "code_discount": code.discount_percent,
            "base_discount": assessment.discount_percent,
        }

    @staticmethod
    def calculate_discounted_price(assessment, discount_code=None):
        """محاسبه قیمت نهایی با احتساب تخفیف پایه و کد"""
        base_price = assessment.final_price

        if base_price == 0:
            return 0

        total_discount = assessment.discount_percent

        if discount_code:
            total_discount += discount_code.discount_percent

        if total_discount > 100:
            total_discount = 100

        return base_price * (100 - total_discount) // 100
