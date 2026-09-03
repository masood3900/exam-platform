import uuid
from django.db import models

from .lesson import Lesson
from .exercise import Exercise


class LessonContent(models.Model):
    """محتوای درس (بخش متنی یا تمرین)"""

    class ContentType(models.TextChoices):
        TEXT = "text", "متن"
        EXERCISE = "exercise", "تمرین"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="contents",
        verbose_name="درس",
    )

    content_type = models.CharField(
        max_length=20,
        choices=ContentType.choices,
        default=ContentType.TEXT,
        verbose_name="نوع محتوا",
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="عنوان بخش",
    )

    text = models.TextField(
        blank=True,
        verbose_name="متن",
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lesson_contents",
        verbose_name="تمرین",
    )

    order = models.PositiveIntegerField(
        default=1,
        verbose_name="ترتیب",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["lesson", "order"]
        verbose_name = "محتوای درس"
        verbose_name_plural = "محتوای درس‌ها"
        indexes = [
            models.Index(fields=["lesson", "order"]),
        ]

    def __str__(self):
        if self.content_type == self.ContentType.TEXT:
            return f"{self.lesson.title} - {self.title or 'متن'}"
        return f"{self.lesson.title} - تمرین {self.order}"