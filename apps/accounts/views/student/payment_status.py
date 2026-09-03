from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.assessments.models import PaymentRequest


class PaymentStatusView(LoginRequiredMixin, TemplateView):
    """صفحه وضعیت درخواست‌های پرداخت"""

    template_name = "dashboard/student/payment_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payment_requests"] = PaymentRequest.objects.filter(
            user=self.request.user,
        ).select_related("assessment").order_by("-created_at")
        return context
