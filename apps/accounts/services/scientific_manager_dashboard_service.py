from django.db.models import Count, Avg, Q

from apps.assessments.models import (
    AssessmentEnrollment,
    ScientificGroup,
    ScientificGroupMembership,
    Question,
    Assessment,
    Attempt,
    Course,
)


class ScientificManagerDashboardService:
    """سرویس داشبورد مدیر علمی"""

    @staticmethod
    def get_managed_groups(user):
        """گروه‌هایی که کاربر مدیر علمیشونه + فرزندها"""
        groups = ScientificGroup.objects.filter(
            memberships__user=user,
            memberships__role=ScientificGroupMembership.Role.SCIENTIFIC_MANAGER,
            memberships__is_active=True,
            is_active=True,
        ).distinct()

        # شامل فرزندها
        all_groups = list(groups)
        for group in groups:
            children = ScientificGroup.objects.filter(parent=group)
            all_groups.extend(children)

        return ScientificGroup.objects.filter(id__in=[g.id for g in all_groups])

    @staticmethod
    def overall_stats(user):
        """آمار کلی گروه‌های تحت مدیریت"""

        groups = ScientificManagerDashboardService.get_managed_groups(user)

        questions = Question.objects.filter(
            scientific_group__in=groups,
            is_active=True,
        )

        designers = ScientificGroupMembership.objects.filter(
            scientific_group__in=groups,
            role=ScientificGroupMembership.Role.QUESTION_DESIGNER,
            is_active=True,
        ).values('user').distinct().count()

        assessments = Assessment.objects.filter(
            scientific_group__in=groups,
            is_active=True,
        )

        attempts = Attempt.objects.filter(
            assessment__in=assessments,
            status=Attempt.Status.GRADED,
        )

        # دانشجوهایی که در آزمون‌های این گروه ثبت‌نام کردن
        students_count = AssessmentEnrollment.objects.filter(
            assessment__in=assessments,
            status="active",
        ).values("user").distinct().count()

        # تعداد موضوع‌ها (گروه‌هایی که parent دارند)
        topics_count = ScientificGroup.objects.filter(
            id__in=[g.id for g in groups if g.parent is not None],
            is_active=True,
        ).count()

        return {
            "groups_count": groups.count(),
            "topics_count": topics_count,
            "questions_count": questions.count(),
            "designers_count": designers,
            "assessments_count": assessments.count(),
            "students_count": students_count,
            "attempts_count": attempts.count(),
            "average_percentage": round(
                attempts.aggregate(avg=Avg("percentage"))["avg"] or 0,
                2,
            ),
        }

    @staticmethod
    def pending_questions(user):
        """سوالات در انتظار تایید"""

        groups = ScientificManagerDashboardService.get_managed_groups(user)

        return Question.objects.filter(
            scientific_group__in=groups,
            status=Question.QuestionStatus.PENDING,
        ).select_related(
            "scientific_group",
        ).order_by("-created_at")

    @staticmethod
    def group_designers(user):
        """طراحان سوال گروه‌های تحت مدیریت"""

        groups = ScientificManagerDashboardService.get_managed_groups(user)

        designers = ScientificGroupMembership.objects.filter(
            scientific_group__in=groups,
            role=ScientificGroupMembership.Role.QUESTION_DESIGNER,
            is_active=True,
        ).select_related("user", "scientific_group")

        result = []
        for membership in designers:
            question_count = Question.objects.filter(
                scientific_group=membership.scientific_group,
                is_active=True,
            ).count()

            result.append({
                "membership": membership,
                "question_count": question_count,
            })

        return result

    @staticmethod
    def group_courses(user):
        """دوره‌های گروه‌های تحت مدیریت"""
        groups = ScientificManagerDashboardService.get_managed_groups(user)
        return Course.objects.filter(
            scientific_group__in=groups,
        ).select_related("scientific_group", "learning_path").order_by("-created_at")

    @staticmethod
    def get_student_groups_summary(user):
        """خلاصه دانشجویان هر گروه"""
        from apps.accounts.services.student_directory_service import StudentDirectoryService

        groups = ScientificManagerDashboardService.get_managed_groups(user)

        result = []
        for group in groups:
            # فقط موضوع‌ها (parent دارن)
            if group.parent:
                students = StudentDirectoryService.get_group_students_summary(group.id)
                if students:
                    avg = sum(s["stats"]["avg"] for s in students) / len(students)
                    result.append({
                        "group": group,
                        "students_count": len(students),
                        "avg_percentage": round(avg, 2),
                    })

        return result

    @staticmethod
    def group_assessments(user):
        """آزمون‌های گروه‌های تحت مدیریت"""

        groups = ScientificManagerDashboardService.get_managed_groups(user)

        return Assessment.objects.filter(
            scientific_group__in=groups,
            is_active=True,
        ).select_related(
            "scientific_group",
        ).order_by("-created_at")
