from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.accounts.services.dashboard_service import DashboardService


class MyPaidAssessmentsView(LoginRequiredMixin, TemplateView):
    """صفحه آزمون‌های خریداری شده من"""

    template_name = "dashboard/student/my_paid_assessments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        assessments = DashboardService.assessments_dashboard(self.request.user)
        
        # فیلتر آزمون‌های پولی
        paid_assessments = [
            item for item in assessments 
            if not item["assessment"].is_free
        ]
        
        context["assessments"] = paid_assessments
        
        return context