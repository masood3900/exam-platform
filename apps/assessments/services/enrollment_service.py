from django.db import transaction
from django.utils import timezone

from apps.assessments.models import (
    Course,
    CourseEnrollment,
)


class EnrollmentService:

    @staticmethod
    @transaction.atomic
    def enroll(
        user,
        course,
    ):
        if not course.is_active:
            raise ValueError(
                "این دوره فعال نیست."
            )

        enrollment, created = (
            CourseEnrollment.objects.get_or_create(
                user=user,
                course=course,
            )
        )

        # دوره رایگان
        if course.is_free:

            enrollment.status = (
                CourseEnrollment
                .Status
                .ACTIVE
            )

            enrollment.payment_status = (
                CourseEnrollment
                .PaymentStatus
                .NOT_REQUIRED
            )

            enrollment.activated_at = (
                enrollment.activated_at
                or timezone.now()
            )

            enrollment.activated_by = (
                enrollment.activated_by
                or user
            )

            enrollment.save(
                update_fields=[
                    "status",
                    "payment_status",
                    "activated_at",
                    "activated_by",
                ]
            )

            return enrollment

        # دوره پولی
        enrollment.status = (
            CourseEnrollment
            .Status
            .PENDING
        )

        enrollment.payment_status = (
            CourseEnrollment
            .PaymentStatus
            .UNPAID
        )

        enrollment.save(
            update_fields=[
                "status",
                "payment_status",
            ]
        )

        return enrollment