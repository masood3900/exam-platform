from django.conf import settings
from django.db import models
import uuid


class ScientificGroup(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="نام گروه علمی",
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="کد گروه علمی",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
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
        ordering = ["name"]
        verbose_name = "گروه علمی"
        verbose_name_plural = "گروه‌های علمی"

    def __str__(self):
        return f"{self.code} - {self.name}"


class ScientificGroupMembership(models.Model):

    class Role(models.TextChoices):
        SCIENTIFIC_MANAGER = (
            "scientific_manager",
            "مدیر علمی",
        )
        QUESTION_DESIGNER = (
            "question_designer",
            "طراح سؤال",
        )
        INSTRUCTOR = (
            "instructor",
            "مدرس",
        )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    scientific_group = models.ForeignKey(
        ScientificGroup,
        on_delete=models.CASCADE,
        related_name="memberships",
        verbose_name="گروه علمی",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scientific_group_memberships",
        verbose_name="کاربر",
    )

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        verbose_name="نقش",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ عضویت",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "scientific_group",
                    "user",
                    "role",
                ],
                name="unique_scientific_group_user_role",
            ),
        ]

        ordering = [
            "scientific_group",
            "user",
            "role",
        ]

        verbose_name = "عضویت گروه علمی"
        verbose_name_plural = "اعضای گروه‌های علمی"

    def __str__(self):
        return (
            f"{self.user} - "
            f"{self.scientific_group.name} - "
            f"{self.get_role_display()}"
        )