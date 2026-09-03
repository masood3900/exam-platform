from django.views.generic import TemplateView

from apps.accounts.mixins import AdminRequiredMixin
from apps.accounts.services.admin_dashboard_service import (
    AdminDashboardService,
)
from apps.assessments.models import PaymentRequest


class AdminDashboardView(
    AdminRequiredMixin,
    TemplateView,
):

    template_name = "dashboard/admin/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["stats"] = AdminDashboardService.overall_stats()
        
        # درخواست‌های پرداخت در انتظار
        context["pending_payments"] = PaymentRequest.objects.filter(
            status=PaymentRequest.Status.PENDING,
        ).select_related(
            "user",
            "assessment",
            "course",
        ).order_by("-created_at")

        return context