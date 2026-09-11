from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.accounts.services.question_designer_dashboard_service import (
    QuestionDesignerDashboardService,
)


class QuestionDesignerDashboardView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = "dashboard/question_designer/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context["stats"] = (
            QuestionDesignerDashboardService.overall_stats(user)
        )
        context["groups"] = (
            QuestionDesignerDashboardService.group_summary(user)
        )
        context["questions"] = (
            QuestionDesignerDashboardService.designer_questions(user)
        )
        context["dashboard_tree"] = (
            QuestionDesignerDashboardService.designer_dashboard_tree(user)
        )

        from apps.accounts.services.user_directory_service import UserDirectoryService
        context["upper_manager"] = UserDirectoryService.get_upper_manager(user)

        # موضوع‌های طراح سوال
        context["designer_topics"] = (
            QuestionDesignerDashboardService.get_designer_groups(user)
        )

        return context
