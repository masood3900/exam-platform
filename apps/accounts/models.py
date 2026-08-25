import uuid

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


    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.get_full_name() or self.username

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