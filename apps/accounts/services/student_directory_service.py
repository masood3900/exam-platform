from django.db.models import Avg

from apps.assessments.models import (
    AssessmentEnrollment,
    Attempt,
)


class StudentDirectoryService:
    """سرویس مدیریت دانشجویان"""

    @staticmethod
    def get_students_by_group(group_id):
        """دانشجویان یک گروه/دوره"""
        return AssessmentEnrollment.objects.filter(
            assessment__scientific_group_id=group_id,
            status="active",
        ).select_related("user", "assessment").order_by("user__first_name")

    @staticmethod
    def get_student_stats(student, group_id):
        """آمار یک دانشجو در یک گروه"""
        attempts = Attempt.objects.filter(
            student=student,
            assessment__scientific_group_id=group_id,
            status="graded",
        )

        return {
            "total": attempts.count(),
            "avg": round(attempts.aggregate(avg=Avg("percentage"))["avg"] or 0, 2),
            "passed": attempts.filter(passed=True).count(),
        }

    @staticmethod
    def get_group_students_summary(group_id):
        """خلاصه دانشجویان یک گروه"""
        students = StudentDirectoryService.get_students_by_group(group_id)

        result = []
        seen_users = set()
        for enrollment in students:
            if enrollment.user_id in seen_users:
                continue
            seen_users.add(enrollment.user_id)

            stats = StudentDirectoryService.get_student_stats(
                enrollment.user, group_id
            )

            result.append({
                "enrollment": enrollment,
                "student": enrollment.user,
                "stats": stats,
            })

        return result
