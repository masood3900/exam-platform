from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.db import models
from apps.education.models import InstructorAssignment
from apps.assessments.models import (
    Attempt,
    Assessment,
    UserLearningPath,
    AttemptQuestion,
)

User = get_user_model()


class InstructorDashboardService:



    @staticmethod
    def recent_assessments(limit=5):

        assessments = (
            Assessment.objects
            .filter(is_active=True)
            .select_related(
                "course",
                "course__learning_path",
            )
            .order_by("-created_at")[:limit]
        )

        result = []

        for assessment in assessments:

            attempts = Attempt.objects.filter(
                assessment=assessment,
                status=Attempt.Status.GRADED,
            )

            result.append(
                {
                    "assessment": assessment,
                    "attempt_count": attempts.count(),
                    "average_percentage": round(
                        attempts.aggregate(
                            avg=Avg("percentage")
                        )["avg"] or 0,
                        2,
                        ),
                    "passed_count": attempts.filter(
                     passed=True
                    ).count(),
                }
            )

        return result

    @staticmethod
    def overall_stats():

        students_count = User.objects.filter(
            groups__name="Students",
            is_active=True,
            learning_paths__is_active=True,
        ).distinct().count()

        assessment_count = Assessment.objects.filter(
            is_active=True,
        ).count()

        attempts = Attempt.objects.filter(
            status=Attempt.Status.GRADED,
        )

        attempt_count = attempts.count()

        average_percentage = (
            attempts.aggregate(
                avg=Avg("percentage")
            )["avg"] or 0
        )

        return {
            "students_count": students_count,
            "assessment_count": assessment_count,
            "attempt_count": attempt_count,
            "average_percentage": round(
                average_percentage,
                2,
            ),
        }
    @staticmethod
    def students(limit=8):

        students = (
            User.objects
            .filter(
                groups__name="Students",
                is_active=True,
                learning_paths__is_active=True,
            )
            .distinct()
            .order_by(
                "first_name",
                "last_name",
                "username",
            )
        )

        if limit is not None:
            students = students[:limit]

        result = []

        for student in students:

            attempts = Attempt.objects.filter(
                student=student,
                status=Attempt.Status.GRADED,
            )

            result.append(
                {
                    "student": student,
                    "attempt_count": attempts.count(),
                    "average_percentage": round(
                        attempts.aggregate(
                            avg=Avg("percentage")
                        )["avg"] or 0,
                        2,
                    ),
                }
            )

        return result
    @staticmethod
    def student_attempts(student):

        attempts = (
            Attempt.objects
            .filter(
                student=student,
                status=Attempt.Status.GRADED,
            )
            .select_related(
                "assessment",
                "assessment__course",
                "assessment__course__learning_path",
            )
            .order_by("-finished_at")
        )

        return attempts


    
    
    @staticmethod
    def student_detail(student,instructor,):
        assignments = (
           InstructorAssignment.objects.filter(
               student=student,
               instructor=instructor,
               is_active=True,
           ).select_related(
               "learning_path",
               "course",
           ).order_by("-started_at")
        )
        if not assignments.exists():
            return None

        attempts = (
            Attempt.objects
            .filter(
                student=student,
                status=Attempt.Status.GRADED,
            )
            .select_related(
                "assessment",
                "assessment__course",
                "assessment__course__learning_path",
            )
            .order_by("-finished_at")
        )

        result = {
            "student": student,
            "assignments": assignments,
            "attempt_count": attempts.count(),

            "average_percentage": round(
                attempts.aggregate(
                    avg=Avg("percentage")
                )["avg"] or 0,
                2,
            ),

            "best_percentage": round(
                attempts.aggregate(
                    best=models.Max("percentage")
                )["best"] or 0,
                2,
            ),

            "passed_count": attempts.filter(
                passed=True
            ).count(),

            "last_attempt": attempts.first(),

            "attempts": attempts,

            "learning_paths": (
                UserLearningPath.objects
                .filter(
                    user=student,
                    is_active=True,
                )
                .select_related(
                    "learning_path",
                )
            ),
        }

        return result

    @staticmethod
    def attempt_detail(attempt):

        attempt_questions = (
            AttemptQuestion.objects
            .filter(
                attempt=attempt,
            )
            .select_related(
                "question",
                "question__learning_objective",
                "question__learning_objective__category",
            )
            .prefetch_related(
                "choices",
            )
            .order_by("order")
        )

        return {
            "attempt": attempt,
            "questions": attempt_questions,
        }