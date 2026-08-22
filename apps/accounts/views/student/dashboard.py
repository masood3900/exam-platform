from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.accounts.services.dashboard_service import DashboardService


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard/index.html"


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


        return context