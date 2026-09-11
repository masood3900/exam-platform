from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.accounts.services.dashboard_service import DashboardService
from apps.accounts.models import User


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard/student/index.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["stats"] = (
            DashboardService.overall_stats(
                self.request.user
            )
        )

        context["learning_paths"] = (
            DashboardService.learning_paths_dashboard(
                self.request.user
            )
        )
        context["assessments"] = (
            DashboardService.assessments_dashboard(
                self.request.user
            )
        )

        # افراد معرفی‌شده
        referred_users = User.objects.filter(
            referred_by=self.request.user
        ).order_by("-date_joined")

        context["referred_users"] = referred_users
        context["referred_users_count"] = referred_users.count()

        return context
