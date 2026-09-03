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
    def get_assigned_students(instructor):
        """دانش‌آموزانی که به این مدرس تخصیص داده شدن"""
        return User.objects.filter(
            instructor_assignments__instructor=instructor,
            instructor_assignments__is_active=True,
            is_active=True,
        ).distinct()

    @staticmethod
    def get_assigned_courses(instructor):
        """دوره‌هایی که این مدرس تدریس می‌کنه"""
        from apps.assessments.models import CourseInstructorAssignment
        
        return CourseInstructorAssignment.objects.filter(
            instructor=instructor,
            is_active=True,
        ).select_related(
            "course",
            "course__learning_path",
        )

    @staticmethod
    def recent_assessments(instructor, limit=5):
        """آزمون‌های اخیر دوره‌های این مدرس"""
        
        # دوره‌های این مدرس
        instructor_courses = InstructorAssignment.objects.filter(
            instructor=instructor,
            is_active=True,
        ).values_list('course_id', flat=True)

        assessments = (
            Assessment.objects
            .filter(
                is_active=True,
                course_id__in=instructor_courses,
            )
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

            result.append({
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
            })

        return result

    @staticmethod
    def overall_stats(instructor):
        """آمار کلی فقط برای این مدرس"""
        
        students = InstructorDashboardService.get_assigned_students(instructor)
        students_count = students.count()

        # آزمون‌های دوره‌های این مدرس
        instructor_courses = InstructorAssignment.objects.filter(
            instructor=instructor,
            is_active=True,
        ).values_list('course_id', flat=True)

        assessment_count = Assessment.objects.filter(
            is_active=True,
            course_id__in=instructor_courses,
        ).count()

        # تلاش‌های دانش‌آموزان این مدرس
        attempts = Attempt.objects.filter(
            student__in=students,
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
    def students(instructor, limit=8):
        """دانش‌آموزان این مدرس با آمارشون"""
        
        students = InstructorDashboardService.get_assigned_students(instructor)
        
        students = students.order_by(
            "first_name",
            "last_name",
            "username",
        )

        if limit is not None:
            students = students[:limit]

        result = []

        for student in students:
            attempts = Attempt.objects.filter(
                student=student,
                status=Attempt.Status.GRADED,
            )

            result.append({
                "student": student,
                "attempt_count": attempts.count(),
                "average_percentage": round(
                    attempts.aggregate(
                        avg=Avg("percentage")
                    )["avg"] or 0,
                    2,
                ),
            })

        return result

    @staticmethod
    def student_attempts(instructor, student):
        """تلاش‌های یک دانش‌آموز خاص (فقط اگه برای این مدرس باشه)"""
        
        # بررسی اینکه دانش‌آموز برای این مدرسه
        is_assigned = InstructorAssignment.objects.filter(
            instructor=instructor,
            student=student,
            is_active=True,
        ).exists()

        if not is_assigned:
            return Attempt.objects.none()

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
    def student_detail(student, instructor):
        """جزئیات یک دانش‌آموز برای این مدرس"""
        
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
                .select_related("learning_path")
            ),
        }

        return result

    @staticmethod
    def attempt_detail(attempt):
        """جزئیات یک تلاش آزمون"""
        
        attempt_questions = (
            AttemptQuestion.objects
            .filter(attempt=attempt)
            .select_related(
                "question",
                "question__learning_objective",
                "question__learning_objective__category",
            )
            .prefetch_related("choices")
            .order_by("order")
        )

        return {
            "attempt": attempt,
            "questions": attempt_questions,
        }