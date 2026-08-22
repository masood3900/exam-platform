from django.views.generic import TemplateView

from apps.accounts.mixins import AdminRequiredMixin
from apps.accounts.services.admin_dashboard_service import (
    AdminDashboardService,
)


class AdminDashboardView(
    AdminRequiredMixin,
    TemplateView,
):

    template_name = "dashboard/admin/index.html"

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        context["stats"] = (
            AdminDashboardService.overall_stats()
        )

        return context