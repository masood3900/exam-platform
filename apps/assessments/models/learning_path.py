import uuid
from django.db import models


class LearningPath(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=200,
        verbose_name="نام مسیر آموزشی",
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="شناسه مسیر",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="مثلا python یا ambulance",
        verbose_name="آیکون",
    )

    color = models.CharField(
        max_length=20,
        default="primary",
        verbose_name="رنگ کارت",
    )

    scientific_group = models.ForeignKey(
        "ScientificGroup",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="learning_paths",
        verbose_name="حوزه",
        help_text="حوزه‌ای که این مسیر زیرمجموعه آن است",
    )

    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="dependent_paths",
        verbose_name="پیش‌نیازهای مسیر",
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش",
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
        ordering = ["order", "name"]
        verbose_name = "مسیر آموزشی"
        verbose_name_plural = "مسیرهای آموزشی"

    def __str__(self):
        return self.name