import uuid
from django.conf import settings
from django.db import models

from .lesson import Lesson


class Exercise(models.Model):
    """تمرین مستقل برای هر درس"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="exercises",
        verbose_name="درس",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان تمرین",
    )

    body = models.TextField(
        verbose_name="متن تمرین/سوال",
        help_text="توضیح کامل تمرین برای کاربر",
    )

    exercise_type = models.CharField(
        max_length=20,
        choices=[
            ("coding", "کدنویسی"),
            ("quiz", "تستی"),
        ],
        default="coding",
        verbose_name="نوع تمرین",
    )

    language = models.CharField(
        max_length=20,
        choices=[
            ("python", "Python"),
            ("javascript", "JavaScript"),
        ],
        default="python",
        verbose_name="زبان برنامه‌نویسی",
    )

    order = models.PositiveIntegerField(
        default=1,
        verbose_name="ترتیب",
    )

    points = models.PositiveIntegerField(
        default=10,
        verbose_name="امتیاز",
        help_text="امتیازی که کاربر با پاسخ درست می‌گیرد",
    )

    starter_code = models.TextField(
        blank=True,
        verbose_name="کد اولیه",
        help_text="کدی که از قبل در ادیتور هست",
    )

    test_input = models.TextField(
        blank=True,
        verbose_name="ورودی تست",
        help_text="ورودی که به برنامه داده می‌شود",
    )

    expected_output = models.TextField(
        blank=True,
        verbose_name="خروجی مورد انتظار",
        help_text="خروجی که برنامه باید تولید کند",
    )

    feedback = models.TextField(
        blank=True,
        verbose_name="بازخورد آموزشی",
        help_text="توضیحی که وقتی کاربر غلط جواب داد نمایش داده می‌شود",
    )
    test_cases = models.JSONField(
        default=list,
        blank=True,
        verbose_name="تست‌کیس‌ها",
        help_text='مثال: [{"input": "5\\n3", "expected": "8"}]',
    )
    
    points_deduction_per_attempt = models.PositiveIntegerField(
        default=2,
        verbose_name="کسر امتیاز هر تلاش",
        help_text="با هر بررسی غلط، چقدر امتیاز کم شود",
    )
    
    minimum_points = models.PositiveIntegerField(
        default=4,
        verbose_name="حداقل امتیاز",
        help_text="کمترین امتیازی که کاربر می‌تواند بگیرد",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["lesson", "order"]
        verbose_name = "تمرین"
        verbose_name_plural = "تمرین‌ها"
        indexes = [
            models.Index(fields=["lesson", "order"]),
        ]

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class ExerciseAttempt(models.Model):
    """تلاش کاربر برای تمرین"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exercise_attempts",
        verbose_name="کاربر",
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="تمرین",
    )

    is_correct = models.BooleanField(
        default=False,
        verbose_name="پاسخ درست",
    )

    score_earned = models.PositiveIntegerField(
        default=0,
        verbose_name="امتیاز کسب شده",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "تلاش تمرین"
        verbose_name_plural = "تلاش‌های تمرین"

    def __str__(self):
        return f"{self.user} - {self.exercise.title}"