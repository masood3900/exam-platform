import uuid
from django.db import models


class PaymentAccount(models.Model):
    """حساب‌های پرداخت ادمین"""

    class AccountType(models.TextChoices):
        CARD = "card", "کارت بانکی"
        SHABA = "shaba", "شماره شبا"
        CRYPTO = "crypto", "کیف پول دیجیتال"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.CARD,
        verbose_name="نوع حساب",
    )

    title = models.CharField(
        max_length=100,
        verbose_name="عنوان",
        help_text="مثلاً: کارت بانک ملی",
    )

    account_number = models.CharField(
        max_length=100,
        verbose_name="شماره حساب/کارت/آدرس کیف پول",
    )

    owner_name = models.CharField(
        max_length=100,
        verbose_name="به نام",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["account_type", "title"]
        verbose_name = "حساب پرداخت"
        verbose_name_plural = "حساب‌های پرداخت"

    def __str__(self):
        return f"{self.get_account_type_display()} - {self.title}"