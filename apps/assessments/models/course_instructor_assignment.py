import uuid

from django.conf import settings
from django.db import models

from .course import Course


class CourseInstructorAssignment(models.Model):

    class Role(models.TextChoices):
        MAIN = (
            "main",
            "مدرس اصلی",
        )
        ASSISTANT = (
            "assistant",
            "مدرس دستیار",
        )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course_instructor_assignments",
        verbose_name="دوره",
    )

    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="course_instructor_assignments",
        verbose_name="مدرس",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MAIN,
        verbose_name="نقش",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ تخصیص",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "course",
                    "instructor",
                    "role",
                ],
                name="unique_course_instructor_assignment",
            ),
        ]

        ordering = [
            "course",
            "role",
            "instructor",
        ]

        verbose_name = "تخصیص مدرس دوره"
        verbose_name_plural = "تخصیص‌های مدرسان دوره"

    def __str__(self):
        return (
            f"{self.instructor} - "
            f"{self.course.name} - "
            f"{self.get_role_display()}"
        )