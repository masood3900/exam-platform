import uuid
from django.db import models

from .course import Course
from .question import QuestionCategory


class Lesson(models.Model):
    """درس‌های داخل هر فصل"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="lessons",
        verbose_name="دوره",
    )

    category = models.ForeignKey(
        QuestionCategory,
        on_delete=models.PROTECT,
        related_name="lessons",
        null=True,
        blank=True,
        verbose_name="فصل",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان درس",
    )

    content = models.TextField(
        blank=True,
        verbose_name="متن درس",
    )

    video = models.FileField(
        upload_to="lessons/videos/",
        null=True,
        blank=True,
        verbose_name="ویدیو",
    )

    attachment = models.FileField(
        upload_to="lessons/attachments/",
        null=True,
        blank=True,
        verbose_name="فایل ضمیمه",
    )

    order = models.PositiveIntegerField(
        default=1,
        verbose_name="ترتیب",
    )

    duration_minutes = models.PositiveIntegerField(
        default=10,
        verbose_name="مدت زمان (دقیقه)",
    )

    is_free = models.BooleanField(
        default=False,
        verbose_name="پیش‌نمایش رایگان",
        help_text="آیا این درس برای کاربران ثبت‌نام نشده قابل مشاهده است؟",
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
        ordering = ["course", "order", "title"]
        verbose_name = "درس"
        verbose_name_plural = "درس‌ها"
        indexes = [
            models.Index(fields=["course", "order"]),
            models.Index(fields=["is_free"]),
        ]

    def __str__(self):
        return f"{self.course.name} - {self.title}"