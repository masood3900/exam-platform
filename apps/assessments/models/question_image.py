import uuid
from django.conf import settings
from django.db import models


class QuestionImage(models.Model):
    """عکس‌های آپلود شده برای سوالات"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_question_images",
        verbose_name="آپلود شده توسط",
    )

    image = models.ImageField(
        upload_to="questions/%Y/%m/",
        verbose_name="عکس",
    )

    original_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="نام اصلی فایل",
    )

    file_size = models.PositiveIntegerField(
        default=0,
        verbose_name="حجم فایل (بایت)",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "عکس سوال"
        verbose_name_plural = "عکس‌های سوالات"

    def __str__(self):
        return f"{self.original_name} - {self.uploaded_by}"
