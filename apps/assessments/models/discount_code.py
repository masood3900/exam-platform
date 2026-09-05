import uuid
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


class DiscountCode(models.Model):
    """کد تخفیف برای آزمون‌ها"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="کد تخفیف",
    )

    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name="درصد تخفیف",
        help_text="درصد تخفیف از 0 تا 100",
    )

    assessment = models.ForeignKey(
        "Assessment",
        on_delete=models.CASCADE,
        related_name="discount_codes",
        null=True,
        blank=True,
        verbose_name="آزمون خاص",
        help_text="اگر خالی باشد، برای همه آزمون‌ها قابل استفاده است",
    )

    valid_from = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ شروع اعتبار",
    )

    valid_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان اعتبار",
    )

    max_uses = models.PositiveIntegerField(
        default=1,
        verbose_name="حداکثر تعداد استفاده",
        help_text="تعداد کل دفعات مجاز استفاده از کد",
    )

    used_count = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد استفاده شده",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_discount_codes",
        verbose_name="ایجاد شده توسط",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["valid_until"]),
        ]

    @property
    def is_valid(self):
        """بررسی اعتبار کد"""
        if not self.is_active:
            return False
        if self.used_count >= self.max_uses:
            return False
        now = timezone.now()
        if self.valid_until and now > self.valid_until:
            return False
        if now < self.valid_from:
            return False
        return True

    @property
    def remaining_uses(self):
        """تعداد استفاده‌های باقی‌مانده"""
        return max(0, self.max_uses - self.used_count)

    def __str__(self):
        return f"{self.code} - {self.discount_percent}%"


class DiscountCodeUsage(models.Model):
    """ثبت استفاده از کد تخفیف"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    code = models.ForeignKey(
        DiscountCode,
        on_delete=models.PROTECT,
        related_name="usages",
        verbose_name="کد تخفیف",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="discount_code_usages",
        verbose_name="کاربر",
    )

    assessment = models.ForeignKey(
        "Assessment",
        on_delete=models.CASCADE,
        related_name="discount_usages",
        verbose_name="آزمون",
    )

    discount_percent = models.PositiveSmallIntegerField(
        verbose_name="درصد تخفیف اعمال شده",
    )

    original_price = models.PositiveIntegerField(
        verbose_name="قیمت اصلی",
    )

    discounted_price = models.PositiveIntegerField(
        verbose_name="قیمت پس از تخفیف",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "استفاده از کد تخفیف"
        verbose_name_plural = "استفاده‌های کد تخفیف"
        constraints = [
            models.UniqueConstraint(
                fields=["code", "user"],
                name="unique_discount_code_per_user",
            ),
        ]

    def __str__(self):
        return f"{self.user} - {self.code.code}"
