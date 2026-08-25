from django.db import transaction
from django.utils import timezone

from apps.assessments.models import (
    Assessment,
    AssessmentEnrollment,
)


class AssessmentEnrollmentService:

    @staticmethod
    @transaction.atomic
    def activate_free_assessment(
        *,
        student,
        assessment,
    ):
        """
        فعال‌سازی مستقیم یک آزمون رایگان.
        """

        if not assessment.is_active:
            raise ValueError(
                "این آزمون فعال نیست."
            )

        if not assessment.is_free:
            raise ValueError(
                "این آزمون رایگان نیست."
            )

        enrollment, created = (
            AssessmentEnrollment.objects.get_or_create(
                user=student,
                assessment=assessment,
                defaults={
                    "status": AssessmentEnrollment.Status.ACTIVE,
                    "payment_status": (
                        AssessmentEnrollment.PaymentStatus.NOT_REQUIRED
                    ),
                    "activated_at": timezone.now(),
                },
            )
        )

        if not created:

            enrollment.status = (
                AssessmentEnrollment.Status.ACTIVE
            )

            enrollment.payment_status = (
                AssessmentEnrollment.PaymentStatus.NOT_REQUIRED
            )

            if not enrollment.activated_at:
                enrollment.activated_at = timezone.now()

            enrollment.save(
                update_fields=[
                    "status",
                    "payment_status",
                    "activated_at",
                ]
            )

        return enrollment

    @staticmethod
    @transaction.atomic
    def activate_paid_assessment(
        *,
        student,
        assessment,
    ):
        """
        فعال‌سازی آزمون پولی پس از تأیید پرداخت.
        """

        if not assessment.is_active:
            raise ValueError(
                "این آزمون فعال نیست."
            )

        if assessment.is_free:
            raise ValueError(
                "این آزمون رایگان است."
            )

        enrollment, created = (
            AssessmentEnrollment.objects.get_or_create(
                user=student,
                assessment=assessment,
                defaults={
                    "status": AssessmentEnrollment.Status.ACTIVE,
                    "payment_status": (
                        AssessmentEnrollment.PaymentStatus.PAID
                    ),
                    "activated_at": timezone.now(),
                },
            )
        )

        if not created:

            enrollment.status = (
                AssessmentEnrollment.Status.ACTIVE
            )

            enrollment.payment_status = (
                AssessmentEnrollment.PaymentStatus.PAID
            )

            if not enrollment.activated_at:
                enrollment.activated_at = timezone.now()

            enrollment.save(
                update_fields=[
                    "status",
                    "payment_status",
                    "activated_at",
                ]
            )

        return enrollment