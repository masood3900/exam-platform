from django.conf import settings
from django.db import models

from .learning_path import LearningPath


class UserLearningPath(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_paths",
        verbose_name="کاربر",
    )

    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.PROTECT,
        related_name="students",
        verbose_name="مسیر آموزشی",
    )

    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ شروع",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان",
    )

    class Meta:
        unique_together = (
            "user",
            "learning_path",
        )

        verbose_name = "مسیر آموزشی کاربر"
        verbose_name_plural = "مسیرهای آموزشی کاربران"

    def __str__(self):
        return f"{self.user} - {self.learning_path}"