import uuid
from django.core.validators import MaxValueValidator
from django.db import models

from .learning_path import LearningPath


class Course(models.Model):

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
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="دوره والد",
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
        validators=[
            MaxValueValidator(100),
        ],
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
        return self.price == 0

    @property
    def final_price(self):
        if self.price == 0:
            return 0

        return self.price * (
            100 - self.discount_percent
        ) // 100

    @property
    def has_discount(self):
        return (
            self.price > 0
            and self.discount_percent > 0
        )


    class Meta:

        ordering = [
            "learning_path",
            "order",
            "name",
        ]

        indexes = [

            models.Index(
                fields=[
                    "learning_path",
                ]
            ),

            models.Index(
                fields=[
                    "is_active",
                ]
            ),

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

        return f"{self.learning_path.name} - {self.name}"