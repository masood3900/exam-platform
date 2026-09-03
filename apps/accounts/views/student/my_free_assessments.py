from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.accounts.services.dashboard_service import DashboardService


class MyFreeAssessmentsView(LoginRequiredMixin, TemplateView):
    """صفحه آزمون‌های رایگان من"""

    template_name = "dashboard/student/my_free_assessments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        assessments = DashboardService.assessments_dashboard(self.request.user)
        
        # فیلتر آزمون‌های رایگان
        free_assessments = [
            item for item in assessments 
            if item["assessment"].is_free
        ]
        
        context["assessments"] = free_assessments
        
        return context