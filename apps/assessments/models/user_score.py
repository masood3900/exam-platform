import uuid
from django.conf import settings
from django.db import models


class UserScore(models.Model):
    """امتیاز کلی کاربر"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="score",
        verbose_name="کاربر",
    )

    total_score = models.PositiveIntegerField(
        default=0,
        verbose_name="امتیاز کل",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "امتیاز کاربر"
        verbose_name_plural = "امتیازهای کاربران"

    def __str__(self):
        return f"{self.user} - {self.total_score} امتیاز"

    @staticmethod
    def get_or_create(user):
        score, created = UserScore.objects.get_or_create(user=user)
        return score

    def add_score(self, points):
        self.total_score += points
        self.save(update_fields=["total_score"])