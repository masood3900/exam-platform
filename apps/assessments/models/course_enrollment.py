from django.conf import settings
from django.db import models

from .course import Course


class CourseEnrollment(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار فعال‌سازی"
        ACTIVE = "active", "فعال"
        CANCELLED = "cancelled", "لغو شده"

    class PaymentStatus(models.TextChoices):
        NOT_REQUIRED = "not_required", "نیازی به پرداخت نیست"
        UNPAID = "unpaid", "پرداخت نشده"
        PAID = "paid", "پرداخت شده"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_enrollments",
        verbose_name="دانش‌آموز",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="enrollments",
        verbose_name="دوره",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="وضعیت دسترسی",
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID,
        verbose_name="وضعیت پرداخت",
    )

    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت‌نام",
    )

    activated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ فعال‌سازی",
    )

    activated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activated_course_enrollments",
        verbose_name="فعال‌سازی توسط",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "course",
                ],
                name="unique_user_course_enrollment",
            ),
        ]

        ordering = [
            "-enrolled_at",
        ]

        verbose_name = "ثبت‌نام دوره"
        verbose_name_plural = "ثبت‌نام‌های دوره"

    @property
    def has_access(self):
        return self.status == self.Status.ACTIVE

    def __str__(self):
        return (
            f"{self.user} - {self.course.name}"
        )