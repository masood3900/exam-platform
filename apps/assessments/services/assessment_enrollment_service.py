import uuid
from django.db import transaction
from django.utils import timezone

from apps.assessments.models import (
    Assessment,
    AssessmentEnrollment,
)


class AssessmentEnrollmentService:

    @staticmethod
    @transaction.atomic
    def enroll(*, student, assessment):
        """ثبت‌نام اولیه در آزمون"""

        if not assessment.is_active:
            raise ValueError("این آزمون فعال نیست.")

        enrollment, created = AssessmentEnrollment.objects.get_or_create(
            user=student,
            assessment=assessment,
        )

        # اگه قبلاً پرداخت شده، دست نزن
        if not created and enrollment.payment_status == AssessmentEnrollment.PaymentStatus.PAID:
            return enrollment

        # آزمون رایگان (قیمت صفر یا تخفیف ۱۰۰٪)
        if assessment.is_free:
            return AssessmentEnrollmentService.activate_free_assessment(
                student=student,
                assessment=assessment,
            )

        # آزمون پولی - کاربر می‌تونه آزمایشی شروع کنه
        enrollment.status = AssessmentEnrollment.Status.ACTIVE
        enrollment.payment_status = AssessmentEnrollment.PaymentStatus.UNPAID
        enrollment.save(update_fields=["status", "payment_status"])

        # اتصال کاربر به گروه علمی آزمون
        if assessment.scientific_group:
            from apps.assessments.models import ScientificGroupMembership
            ScientificGroupMembership.objects.get_or_create(
                user=student,
                scientific_group=assessment.scientific_group,
                role="student",
                defaults={"is_active": True},
            )

        return enrollment

    @staticmethod
    @transaction.atomic
    def activate_free_assessment(*, student, assessment):
        """فعال‌سازی مستقیم یک آزمون رایگان"""

        if not assessment.is_active:
            raise ValueError("این آزمون فعال نیست.")

        if not assessment.is_free:
            raise ValueError("این آزمون رایگان نیست.")

        enrollment, created = AssessmentEnrollment.objects.get_or_create(
            user=student,
            assessment=assessment,
            defaults={
                "status": AssessmentEnrollment.Status.ACTIVE,
                "payment_status": AssessmentEnrollment.PaymentStatus.NOT_REQUIRED,
                "activated_at": timezone.now(),
            },
        )

        if not created:
            enrollment.status = AssessmentEnrollment.Status.ACTIVE
            enrollment.payment_status = AssessmentEnrollment.PaymentStatus.NOT_REQUIRED
            if not enrollment.activated_at:
                enrollment.activated_at = timezone.now()
            enrollment.save(update_fields=["status", "payment_status", "activated_at"])

        return enrollment

    @staticmethod
    @transaction.atomic
    def activate_paid_assessment(*, student, assessment):
        """فعال‌سازی آزمون پولی پس از تأیید پرداخت"""

        if not assessment.is_active:
            raise ValueError("این آزمون فعال نیست.")

        if assessment.is_free:
            raise ValueError("این آزمون رایگان است.")

        enrollment, created = AssessmentEnrollment.objects.get_or_create(
            user=student,
            assessment=assessment,
            defaults={
                "status": AssessmentEnrollment.Status.ACTIVE,
                "payment_status": AssessmentEnrollment.PaymentStatus.PAID,
                "activated_at": timezone.now(),
            },
        )

        if not created:
            enrollment.status = AssessmentEnrollment.Status.ACTIVE
            enrollment.payment_status = AssessmentEnrollment.PaymentStatus.PAID
            if not enrollment.activated_at:
                enrollment.activated_at = timezone.now()
            enrollment.save(update_fields=["status", "payment_status", "activated_at"])

        # افزایش max_attempts بعد از پرداخت
        if assessment.max_attempts <= assessment.demo_attempts:
            assessment.max_attempts = assessment.demo_attempts + 10
            assessment.save(update_fields=["max_attempts"])

        return enrollment

    @staticmethod
    @transaction.atomic
    def create_assessment(*, title, assessment_type, description="", price=0,
                          discount_percent=0, duration_minutes=30, passing_score=70,
                          max_attempts=1, demo_attempts=1, scientific_group=None,
                          course=None, is_public=False, created_by=None,
                          source_courses=None):
        """ساخت آزمون جدید"""
        
        code = f"ASSESS-{uuid.uuid4().hex[:8].upper()}"
        
        learning_path = course.learning_path if course else None
        
        if course:
            price = 0
            discount_percent = 0
            if course.scientific_group:
                scientific_group = course.scientific_group
        
        assessment = Assessment.objects.create(
            code=code,
            title=title,
            assessment_type=assessment_type,
            description=description,
            price=price,
            discount_percent=discount_percent,
            duration_minutes=duration_minutes,
            passing_score=passing_score,
            max_attempts=max_attempts,
            demo_attempts=demo_attempts,
            scientific_group=scientific_group,
            course=course,
            learning_path=learning_path,
            is_public=is_public,
            created_by=created_by,
        )
        
        if source_courses:
            assessment.source_courses.set(source_courses)
        
        return assessment