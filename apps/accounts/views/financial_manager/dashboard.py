from django.db.models import Sum
from django.views.generic import TemplateView

from apps.accounts.mixins import LoginRequiredMixin
from apps.assessments.models import PaymentRequest


class FinancialManagerDashboardView(LoginRequiredMixin, TemplateView):
    """داشبورد مدیر مالی"""

    template_name = "dashboard/financial_manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["pending_payments"] = PaymentRequest.objects.filter(
            status=PaymentRequest.Status.PENDING,
        ).select_related("user", "assessment", "course").order_by("-created_at")
        
        context["approved_payments"] = PaymentRequest.objects.filter(
            status=PaymentRequest.Status.APPROVED,
        ).select_related("user", "assessment", "course").order_by("-reviewed_at")[:10]
        
        context["total_revenue"] = PaymentRequest.objects.filter(
            status=PaymentRequest.Status.APPROVED,
        ).aggregate(total=Sum("amount"))["total"] or 0

        # لیست حوزه‌ها برای نمودار
        from apps.assessments.models import ScientificGroup
        context["domains"] = ScientificGroup.objects.filter(parent=None, is_active=True)
        
        return context