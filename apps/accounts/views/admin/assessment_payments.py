from django.views.generic import TemplateView

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import Assessment, PaymentRequest


class AdminAssessmentPaymentsView(AdminRequiredMixin, TemplateView):
    """پرداخت‌های یک آزمون"""

    template_name = "dashboard/admin/assessment_payments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assessment_id = self.kwargs["assessment_id"]

        assessment = Assessment.objects.get(id=assessment_id)
        payments = PaymentRequest.objects.filter(
            assessment=assessment,
        ).select_related("user").order_by("-created_at")

        context["assessment"] = assessment
        context["payments"] = payments
        return context
