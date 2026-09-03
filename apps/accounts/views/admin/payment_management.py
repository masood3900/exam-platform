from django.views.generic import TemplateView
from django.db.models import Sum

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import Assessment, PaymentRequest


class AdminPaymentManagementView(AdminRequiredMixin, TemplateView):
    """مدیریت پرداخت‌ها - لیست آزمون‌ها"""

    template_name = "dashboard/admin/payment_management.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # فقط آزمون‌هایی که پرداخت دارن
        assessments = Assessment.objects.filter(
            payment_requests__isnull=False,
        ).distinct()

        # آمار کلی
        all_payments = PaymentRequest.objects.all()
        context["total_revenue"] = all_payments.filter(status="approved").aggregate(total=Sum("amount"))["total"] or 0
        context["approved_count"] = all_payments.filter(status="approved").count()
        context["pending_count"] = all_payments.filter(status="pending").count()
        context["rejected_count"] = all_payments.filter(status="rejected").count()

        cards = []
        for assessment in assessments:
            payments = PaymentRequest.objects.filter(assessment=assessment)
            cards.append({
                "assessment": assessment,
                "total": payments.count(),
                "approved": payments.filter(status="approved").count(),
                "pending": payments.filter(status="pending").count(),
                "rejected": payments.filter(status="rejected").count(),
            })

        context["cards"] = cards
        return context
