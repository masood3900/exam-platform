from apps.assessments.models import (
    Assessment,
    AssessmentEnrollment,
)


class UserRoleTransitionService:
    """سرویس تبدیل نقش کاربران"""

    @staticmethod
    def guest_to_student_via_assessment(user, assessment):
        """تبدیل مهمان به دانشجو با ثبت‌نام در آزمون"""
        
        if not assessment.is_active:
            raise ValueError("آزمون فعال نیست.")
        
        enrollment, created = AssessmentEnrollment.objects.get_or_create(
            user=user,
            assessment=assessment,
            defaults={
                "status": AssessmentEnrollment.Status.ACTIVE,
                "payment_status": (
                    AssessmentEnrollment.PaymentStatus.NOT_REQUIRED
                    if assessment.is_free
                    else AssessmentEnrollment.PaymentStatus.UNPAID
                ),
            },
        )
        
        return enrollment

    @staticmethod
    def student_to_guest(user):
        """تبدیل دانشجو به مهمان (حذف همه آزمون‌ها)"""
        
        deleted_count, _ = AssessmentEnrollment.objects.filter(user=user).delete()
        
        # چک کن واقعاً چیزی باقی نمونده
        has_any_enrollment = AssessmentEnrollment.objects.filter(user=user).exists()
        has_any_membership = user.scientific_group_memberships.filter(is_active=True).exists()
        
        if not has_any_enrollment and not has_any_membership:
            return True
        return False

    @staticmethod
    def manager_add_student_to_assessment(user, assessment):
        """مدیر علمی دانشجو به آزمون رایگان اضافه می‌کنه"""
        
        if not assessment.is_free:
            raise ValueError("فقط آزمون‌های رایگان قابل انتصاب هستند.")
        
        if not assessment.is_active:
            raise ValueError("آزمون فعال نیست.")
        
        enrollment, created = AssessmentEnrollment.objects.get_or_create(
            user=user,
            assessment=assessment,
            defaults={
                "status": AssessmentEnrollment.Status.ACTIVE,
                "payment_status": AssessmentEnrollment.PaymentStatus.NOT_REQUIRED,
            },
        )
        
        return enrollment

    @staticmethod
    def get_guests():
        """لیست مهمان‌ها"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        return User.objects.exclude(
            scientific_group_memberships__is_active=True,
        ).exclude(
            assessment_enrollments__isnull=False,
        ).exclude(is_staff=True).distinct()

    @staticmethod
    def is_guest(user):
        """چک کن کاربر مهمان هست یا نه"""
        has_membership = user.scientific_group_memberships.filter(is_active=True).exists()
        has_enrollment = AssessmentEnrollment.objects.filter(user=user).exists()
        
        return not has_membership and not has_enrollment and not user.is_staff