from django.db.models import Avg
from django.utils import timezone
from apps.education.models import InstructorAssignment
from apps.assessments.models import (
    UserLearningPath,
    Attempt,
    Assessment,
)
from apps.assessments.models import PaymentRequest




class DashboardService:
    @staticmethod
    def overall_stats(user):
        attempts = Attempt.objects.filter(
            student = user,
            status=Attempt.Status.GRADED,
        )
        today_attempts = attempts.filter(
            finished_at__date=timezone.localdate(),
        )
        average_score = (
            attempts.aggregate(
                avg=Avg("percentage")
            )["avg"] or 0
        )
        best_score = (
            attempts.order_by(
                "-percentage"
            ).values_list(
                "percentage",
                flat=True,

            )
            .first()
            or 0
        )
        return{
            "total_attempts":attempts.count(),
            "average_score":round(
                average_score,
                2,
            ),
            "best_score": best_score,
            "today_attempts": today_attempts.count(),
        }


    @staticmethod
    def learning_paths_dashboard(user):

        user_paths = UserLearningPath.objects.filter(
            user=user,
            is_active=True,
        ).select_related(
            "learning_path",
        )

        result = []

        for user_path in user_paths:

            path = user_path.learning_path

            instructor_assignment = (
                InstructorAssignment.objects
                .filter(
                    student=user,
                    learning_path=path,
                    is_active=True,
                )
                .select_related(
                    "instructor",
                )
                .first()
            )

            attempts = Attempt.objects.filter(
                student=user,
                assessment__course__learning_path=path,
                status=Attempt.Status.GRADED,
            )
            has_attempt = attempts.exists()

            result.append(
                {
                    "learning_path": path,
                    "instructor_assignment": instructor_assignment,
    
                    "assessment_count":Assessment.objects.filter(
                        course__learning_path=path
                    ).count(),
                        
                    "attempt_count": attempts.count(),

                    "has_attempt": has_attempt,
                        
                    "average_percentage":
                        round(
                            attempts.aggregate(
                                avg=Avg("percentage")
                            )["avg"] or 0,
                            2,
                        ),

                    "passed_count":
                        attempts.filter(
                            passed=True
                        ).count(),

                    "last_attempt":
                        attempts.order_by(
                            "-finished_at"
                        ).first(),

                    "status":
                        "در حال یادگیری"
                        if has_attempt
                        else "شروع نشده",
                }
            )

        return result
    @staticmethod
    def assessments_dashboard(user):
        """آزمون‌های ثبت‌نام شده کاربر"""

        from apps.assessments.models import AssessmentEnrollment, PaymentRequest

        enrollments = AssessmentEnrollment.objects.filter(
            user=user,
        ).select_related(
            "assessment",
            "assessment__scientific_group",
            "assessment__course",
        ).order_by("-enrolled_at")

        result = []

        for enrollment in enrollments:
            assessment = enrollment.assessment

            # تعداد تلاش‌های استفاده شده
            used_attempts = Attempt.objects.filter(
                student=user,
                assessment=assessment,
            ).exclude(
                status=Attempt.Status.CREATED,
            ).exclude(
                status=Attempt.Status.CANCELLED,
            ).count()

            # آیا درخواست پرداخت در انتظار داره؟
            has_payment_request = PaymentRequest.objects.filter(
                user=user,
                assessment=assessment,
                status=PaymentRequest.Status.PENDING,
            ).exists()

            result.append({
                "enrollment": enrollment,
                "assessment": assessment,
                "used_attempts": used_attempts,
                "has_access": enrollment.has_access,
                "has_payment_request": has_payment_request,
            })

        return result