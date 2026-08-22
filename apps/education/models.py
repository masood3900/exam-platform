from django.conf import settings
from django.db import models
from django.db.models import Q

from apps.assessments.models import (
    LearningPath,
    Course,
)


class InstructorAssignment(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="instructor_assignments",
        verbose_name="دانش‌آموز",
    )

    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="student_assignments",
        verbose_name="مدرس",
    )

    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="instructor_assignments",
        verbose_name="مسیر آموزشی",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="instructor_assignments",
        verbose_name="دوره آموزشی",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ شروع",
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        verbose_name = "تخصیص مدرس"
        verbose_name_plural = "تخصیص‌های مدرس"

        ordering = [
            "-started_at",
        ]

        constraints = [

            models.CheckConstraint(
                condition=(
                    Q(learning_path__isnull=False)
                    |
                    Q(course__isnull=False)
                ),
                name="assignment_has_learning_scope",
            ),

        ]

        indexes = [

            models.Index(
                fields=[
                    "student",
                    "is_active",
                ]
            ),

            models.Index(
                fields=[
                    "instructor",
                    "is_active",
                ]
            ),

            models.Index(
                fields=[
                    "learning_path",
                ]
            ),

            models.Index(
                fields=[
                    "course",
                ]
            ),

        ]

    def __str__(self):

        return (
            f"{self.student} ← {self.instructor}"
        )