from django.db.models import Count, Avg

from apps.assessments.models import (
    Question,
    ScientificGroup,
    ScientificGroupMembership,
    LearningObjective,
)


class QuestionDesignerDashboardService:
    """سرویس داشبورد طراح سوال"""

    @staticmethod
    def get_designer_groups(user):
        """گروه‌هایی که کاربر در آنها طراح سوال است"""
        return ScientificGroup.objects.filter(
            memberships__user=user,
            memberships__role=ScientificGroupMembership.Role.QUESTION_DESIGNER,
            memberships__is_active=True,
            is_active=True,
        ).distinct()

    @staticmethod
    def overall_stats(user):
        """آمار کلی سوالات طراح"""

        groups = QuestionDesignerDashboardService.get_designer_groups(user)

        all_questions = Question.objects.filter(
            scientific_group__in=groups,
        )

        return {
            "groups_count": groups.count(),
            "total_questions": all_questions.count(),
            "active_questions": all_questions.filter(status="approved").count(),
            "inactive_questions": all_questions.filter(status="pending").count(),
        }

    @staticmethod
    def designer_questions(user, status=None):
        """سوالات گروه‌های طراح"""

        groups = QuestionDesignerDashboardService.get_designer_groups(user)

        questions = Question.objects.filter(
            scientific_group__in=groups,
        ).select_related(
            "scientific_group",
        ).order_by("-created_at")

        if status == "active":
            questions = questions.filter(is_active=True)
        elif status == "inactive":
            questions = questions.filter(is_active=False)

        return questions

    @staticmethod
    def group_summary(user):
        """خلاصه هر گروه برای طراح"""

        groups = QuestionDesignerDashboardService.get_designer_groups(user)

        result = []
        for group in groups:
            questions = Question.objects.filter(
                scientific_group=group,
            )

            result.append({
                "group": group,
                "total": questions.count(),
                "active": questions.filter(is_active=True).count(),
                "inactive": questions.filter(is_active=False).count(),
            })

        return result

    @staticmethod
    def designer_dashboard_tree(user):
        """ساختار درختی: دوره → اهداف → سوالات"""

        groups = QuestionDesignerDashboardService.get_designer_groups(user)

        result = []
        for group in groups:
            objectives = LearningObjective.objects.filter(
                scientific_group=group,
                is_active=True,
            ).order_by("order", "code")

            objective_list = []
            for objective in objectives:
                questions = Question.objects.filter(
                    scientific_group=group,
                    learning_objective=objective,
                ).select_related(
                    "scientific_group",
                    "learning_objective",
                )

                objective_list.append({
                    "objective": objective,
                    "total": questions.count(),
                    "pending": questions.filter(status=Question.QuestionStatus.PENDING).count(),
                    "approved": questions.filter(status=Question.QuestionStatus.APPROVED).count(),
                    "questions": questions.order_by("-created_at"),
                })

            result.append({
                "group": group,
                "objectives": objective_list,
            })

        return result

    @staticmethod
    def designer_questions_by_category(user):
        """سوالات دسته‌بندی شده"""

        groups = QuestionDesignerDashboardService.get_designer_groups(user)

        questions = Question.objects.filter(
            scientific_group__in=groups,
        ).select_related(
            "scientific_group",
        ).order_by(
            "scientific_group__name",
            "code",
        )

        categorized = {}
        for question in questions:
            group_name = question.scientific_group.name if question.scientific_group else "بدون گروه"

            if group_name not in categorized:
                categorized[group_name] = {
                    "group": question.scientific_group,
                    "questions": []
                }

            categorized[group_name]["questions"].append(question)

        return categorized

    @staticmethod
    def designer_questions_by_status(user, status=None):
        """سوالات طراح بر اساس وضعیت"""

        groups = QuestionDesignerDashboardService.get_designer_groups(user)

        questions = Question.objects.filter(
            scientific_group__in=groups,
        )

        if status:
            questions = questions.filter(status=status)

        return questions.select_related(
            "scientific_group",
        ).order_by("-created_at")

    @staticmethod
    def get_question_details(user, question_id):
        """دریافت جزئیات یک سوال"""

        groups = QuestionDesignerDashboardService.get_designer_groups(user)

        question = Question.objects.filter(
            id=question_id,
            scientific_group__in=groups,
        ).select_related(
            "scientific_group",
            "reviewed_by",
        ).prefetch_related(
            "choices",
            "review_history",
        ).first()

        return question
