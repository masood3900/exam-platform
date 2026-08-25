from apps.assessments.models import (
    Assessment,
    AssessmentEnrollment,
    Attempt,
)


class AssessmentAccessService:

    @staticmethod
    def get_enrollment(
        user,
        assessment,
    ):
        return (
            AssessmentEnrollment.objects
            .filter(
                user=user,
                assessment=assessment,
            )
            .first()
        )

    @staticmethod
    def used_attempts(
        user,
        assessment,
    ):
        return Attempt.objects.filter(
            student=user,
            assessment=assessment,
        ).exclude(
            status=Attempt.Status.CREATED,
        ).exclude(
            status=Attempt.Status.CANCELLED,
        ).count()

    @staticmethod
    def can_start(
        user,
        assessment,
    ):
        enrollment = (
            AssessmentAccessService
            .get_enrollment(
                user,
                assessment,
            )
        )

        used_attempts = (
            AssessmentAccessService
            .used_attempts(
                user,
                assessment,
            )
        )

        # آزمون رایگان
        if assessment.is_free:

            if enrollment is None:
                enrollment = (
                    AssessmentEnrollment.objects.create(
                        user=user,
                        assessment=assessment,
                        status=(
                            AssessmentEnrollment.Status.ACTIVE
                        ),
                        payment_status=(
                            AssessmentEnrollment.PaymentStatus
                            .NOT_REQUIRED
                        ),
                    )
                )

            return enrollment.has_access

        # آزمون پولی
        if enrollment:

            # خرید انجام شده
            if (
                enrollment.payment_status
                == AssessmentEnrollment.PaymentStatus.PAID
            ):
                return (
                    enrollment.has_access
                    and used_attempts
                    < assessment.max_attempts
                )

        # تلاش آزمایشی
        return (
            used_attempts
            < assessment.demo_attempts
        )