import uuid

import random
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    GENDER_CHOICES = (
        ("M", "مرد"),
        ("F", "زن"),
    )

    username = models.CharField(
        "نام کاربری",
        max_length=150,
        unique=True,
    )

    first_name = models.CharField(
        "نام",
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        "نام خانوادگی",
        max_length=150,
        blank=True,
    )

    email = models.EmailField(
        "ایمیل",
        blank=True,
    )

    national_code = models.CharField(
        "کد ملی",
        max_length=10,
        unique=True,
        null=True,
        blank=True,
    )

    phone = models.CharField(
        "شماره موبایل",
        max_length=11,
        null=True,
        blank=True,
    )

    birth_date = models.DateField(
        "تاریخ تولد",
        null=True,
        blank=True,
    )

    gender = models.CharField(
        "جنسیت",
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )
   

    avatar = models.ImageField(
        "تصویر پروفایل",
        upload_to="avatars/",
        null=True,
        blank=True,
    )

    # اطلاعات بانکی
    bank_account_number = models.CharField(
        "شماره حساب",
        max_length=30,
        blank=True,
        help_text="شماره حساب یا شماره کارت برای واریز وجه",
    )

    bank_name = models.CharField(
        "نام بانک",
        max_length=50,
        blank=True,
    )

    # کد معرف
    referral_code = models.CharField(
        "کد معرف",
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        help_text="کد اختصاصی معرفی کاربران",
    )

    referred_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referred_users",
        verbose_name="معرفی شده توسط",
    )

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.get_full_name() or self.username

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)

    def generate_referral_code(self):
        """ساخت کد معرف یکتا"""
        while True:
            code = f"SJ{random.randint(10000, 99999)}"
            if not User.objects.filter(referral_code=code).exists():
                return code


class UserProfile(models.Model):

    class Gender(models.TextChoices):
        MALE = "M", "مرد"
        FEMALE = "F", "زن"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    national_code = models.CharField(
        "کد ملی",
        max_length=10,
        unique=True,
        blank=True,
        null=True,
    )

    phone = models.CharField(
        "شماره موبایل",
        max_length=11,
        blank=True,
    )

    birth_date = models.DateField(
        "تاریخ تولد",
        null=True,
        blank=True,
    )

    gender = models.CharField(
        "جنسیت",
        max_length=1,
        choices=Gender.choices,
        blank=True,
    )

    avatar = models.ImageField(
        "تصویر پروفایل",
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    email_verified = models.BooleanField(
        default=False,
    )

    phone_verified = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل کاربران"

    def __str__(self):
        return self.user.username

from apps.accounts.models_wallet import Wallet, Transaction
