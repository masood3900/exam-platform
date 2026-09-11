import uuid
from django.conf import settings
from django.db import models


class Wallet(models.Model):
    """کیف پول کاربر"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet",
        verbose_name="کاربر",
    )

    balance = models.DecimalField(
        "موجودی",
        max_digits=15,
        decimal_places=0,
        default=0,
        help_text="موجودی به تومان",
    )

    is_active = models.BooleanField(
        "فعال",
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف پول‌ها"

    def __str__(self):
        return f"{self.user} - {self.balance:,} تومان"

    def add_balance(self, amount, description="", related_object=None):
        """افزایش موجودی"""
        self.balance += amount
        self.save(update_fields=["balance", "updated_at"])

        Transaction.objects.create(
            wallet=self,
            transaction_type=Transaction.Type.DEPOSIT,
            amount=amount,
            balance_after=self.balance,
            description=description,
        )

    def deduct_balance(self, amount, description="", related_object=None):
        """کاهش موجودی"""
        if self.balance < amount:
            raise ValueError("موجودی کافی نیست.")

        self.balance -= amount
        self.save(update_fields=["balance", "updated_at"])

        Transaction.objects.create(
            wallet=self,
            transaction_type=Transaction.Type.WITHDRAW,
            amount=-amount,
            balance_after=self.balance,
            description=description,
        )


class Transaction(models.Model):
    """تراکنش کیف پول"""

    class Type(models.TextChoices):
        DEPOSIT = "deposit", "واریز"
        WITHDRAW = "withdraw", "برداشت"
        PURCHASE = "purchase", "خرید"
        REVENUE_SHARE = "revenue_share", "سهم فروش"
        REFERRAL_BONUS = "referral_bonus", "پاداش معرف"
        DESIGNER_PAYMENT = "designer_payment", "پرداخت طراح"
        REFUND = "refund", "بازگشت وجه"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="کیف پول",
    )

    transaction_type = models.CharField(
        "نوع تراکنش",
        max_length=30,
        choices=Type.choices,
    )

    amount = models.DecimalField(
        "مبلغ",
        max_digits=15,
        decimal_places=0,
        help_text="مثبت = واریز، منفی = برداشت",
    )

    balance_after = models.DecimalField(
        "موجودی بعد از تراکنش",
        max_digits=15,
        decimal_places=0,
    )

    description = models.TextField(
        "توضیحات",
        blank=True,
    )

    related_id = models.CharField(
        "شناسه مرتبط",
        max_length=100,
        blank=True,
        help_text="مثلاً شناسه پرداخت یا آزمون",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"
        indexes = [
            models.Index(fields=["wallet", "-created_at"]),
            models.Index(fields=["transaction_type"]),
        ]

    def __str__(self):
        return f"{self.wallet.user} - {self.get_transaction_type_display()} - {self.amount:,}"
