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
    def can_start(user, assessment):
        """بررسی آیا کاربر می‌تواند آزمون را شروع کند"""
        
        enrollment = AssessmentAccessService.get_enrollment(user, assessment)
        used_attempts = AssessmentAccessService.used_attempts(user, assessment)

        # آزمون رایگان → بی‌نهایت
        if assessment.is_free:
            if enrollment is None:
                enrollment = AssessmentEnrollment.objects.create(
                    user=user,
                    assessment=assessment,
                    status=AssessmentEnrollment.Status.ACTIVE,
                    payment_status=AssessmentEnrollment.PaymentStatus.NOT_REQUIRED,
                )
            return enrollment.has_access

        # آزمون پولی
        if enrollment:
            # پرداخت شده → طبق max_attempts
            if enrollment.payment_status == AssessmentEnrollment.PaymentStatus.PAID:
                return (
                    enrollment.has_access
                    and used_attempts < assessment.max_attempts
                )
            
            # پرداخت نشده → فقط تلاش آزمایشی
            return used_attempts < assessment.demo_attempts

        # بدون ثبت‌نام → تلاش آزمایشی
        return used_attempts < assessment.demo_attempts
    @staticmethod
    def can_user_access(user, assessment):
        """بررسی آیا کاربر به آزمون دسترسی دارد یا خیر"""
        
        # ادمین همیشه دسترسی داره
        if user.is_staff or user.is_superuser:
            return True
        
        # آزمون رایگان
        if assessment.is_free:
            return True
        
        # بررسی ثبت‌نام
        enrollment = AssessmentAccessService.get_enrollment(
            user,
            assessment,
        )
        
        if enrollment:
            # ثبت‌نام فعال
            if enrollment.has_access:
                return True
            
            # پرداخت شده
            if enrollment.payment_status == AssessmentEnrollment.PaymentStatus.PAID:
                return True
        
        # تلاش آزمایشی
        used_attempts = AssessmentAccessService.used_attempts(
            user,
            assessment,
        )
        
        return used_attempts < assessment.demo_attempts