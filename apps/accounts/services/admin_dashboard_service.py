from apps.accounts.models import User
from apps.assessments.models import (
    Course,
    Assessment,
    Question,
)


class AdminDashboardService:

    @staticmethod
    def overall_stats():

        return {
            "students": User.objects.filter(
                groups__name="Students",
                is_active=True,
            ).distinct().count(),

            "courses": Course.objects.filter(
                is_active=True,
                parent__isnull=False,
            ).count(),

            "assessments": Assessment.objects.filter(
                is_active=True,
            ).count(),

            "questions": Question.objects.filter(
                is_active=True,
            ).count(),
        }