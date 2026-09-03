import uuid
from django.conf import settings
from django.db import models


class PaymentRequest(models.Model):
    """درخواست پرداخت برای فعال‌سازی"""

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار بررسی"
        APPROVED = "approved", "تایید شده"
        REJECTED = "rejected", "رد شده"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payment_requests",
        verbose_name="دانش‌آموز",
    )

    assessment = models.ForeignKey(
        "Assessment",
        on_delete=models.PROTECT,
        related_name="payment_requests",
        verbose_name="آزمون",
        null=True,
        blank=True,
    )

    course = models.ForeignKey(
        "Course",
        on_delete=models.PROTECT,
        related_name="payment_requests",
        verbose_name="دوره",
        null=True,
        blank=True,
    )

    amount = models.PositiveIntegerField(
        verbose_name="مبلغ (تومان)",
    )

    tracking_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="کد رهگیری",
    )

    receipt_image = models.ImageField(
        upload_to="payment_receipts/",
        null=True,
        blank=True,
        verbose_name="عکس رسید",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="وضعیت",
    )

    admin_note = models.TextField(
        blank=True,
        verbose_name="یادداشت ادمین",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ارسال",
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ بررسی",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "درخواست پرداخت"
        verbose_name_plural = "درخواست‌های پرداخت"

    def __str__(self):
        return f"{self.user} - {self.amount} تومان"