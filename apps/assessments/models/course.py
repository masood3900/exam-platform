import uuid
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models

from .learning_path import LearningPath


class Course(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "پیش‌نویس"
        PENDING = "pending", "در انتظار تایید"
        PUBLISHED = "published", "منتشر شده"
        REJECTED = "rejected", "رد شده"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name="مسیر آموزشی",
        null=True,
        blank=True,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="دوره والد",
    )

    scientific_group = models.ForeignKey(
        "ScientificGroup",
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name="گروه علمی",
        null=True,
        blank=True,
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="کد دوره",
    )

    name = models.CharField(
        max_length=255,
        verbose_name="نام دوره",
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات دوره",
    )

    price = models.PositiveIntegerField(
        default=0,
        verbose_name="قیمت دوره",
        help_text="قیمت پایه دوره به تومان؛ صفر یعنی رایگان",
    )

    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(100)],
        verbose_name="درصد تخفیف",
        help_text="درصد تخفیف از 0 تا 100",
    )

    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="dependent_courses",
        verbose_name="پیش‌نیازهای دوره",
    )

    order = models.PositiveIntegerField(
        default=1,
        verbose_name="ترتیب نمایش",
    )

    estimated_minutes = models.PositiveIntegerField(
        default=60,
        verbose_name="زمان تقریبی یادگیری (دقیقه)",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="وضعیت انتشار",
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ انتشار",
    )

    review_note = models.TextField(
        blank=True,
        verbose_name="یادداشت بررسی",
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_courses",
        verbose_name="بررسی شده توسط",
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

    @property
    def is_free(self):
        return self.final_price == 0

    @property
    def final_price(self):
        if self.price == 0:
            return 0
        return self.price * (100 - self.discount_percent) // 100

    @property
    def has_discount(self):
        return self.price > 0 and self.discount_percent > 0

    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED

    class Meta:
        ordering = ["learning_path", "order", "name"]
        indexes = [
            models.Index(fields=["learning_path"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["status"]),
        ]
        verbose_name = "دوره آموزشی"
        verbose_name_plural = "دوره‌های آموزشی"

    @property
    def has_prerequisites(self):
        return self.prerequisites.exists()

    @property
    def prerequisite_count(self):
        return self.prerequisites.count()

    @property
    def is_root(self):
        return self.parent is None

    def __str__(self):
        if self.parent:
            return f"{self.parent} > {self.name}"
        return f"{self.learning_path.name if self.learning_path else ''} - {self.name}"