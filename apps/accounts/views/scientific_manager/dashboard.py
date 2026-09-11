from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.accounts.services.scientific_manager_dashboard_service import (
    ScientificManagerDashboardService,
)
from apps.accounts.models import User


class ScientificManagerDashboardView(
    LoginRequiredMixin,
    TemplateView,
):

    template_name = "dashboard/scientific_manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context["stats"] = (
            ScientificManagerDashboardService.overall_stats(user)
        )
        context["pending_questions"] = (
            ScientificManagerDashboardService.pending_questions(user)
        )
        context["designers"] = (
            ScientificManagerDashboardService.group_designers(user)
        )
        context["group_courses"] = (
            ScientificManagerDashboardService.group_courses(user)
        )
        context["assessments"] = (
            ScientificManagerDashboardService.group_assessments(user)
        )
        
        # کاربران برای افزودن طراح
        context["all_users"] = User.objects.filter(is_active=True)
        
        # مسیرهای آموزشی تحت مدیریت (فقط فرزندان مستقیم رشته‌ها)
        context["my_groups"] = (
            ScientificManagerDashboardService.get_managed_groups(user).filter(
                parent__isnull=False,
                parent__parent__isnull=True,
            )
        )

        # موضوع‌های تحت مدیریت (فرزندان مسیرها)
        context["managed_topics"] = (
            ScientificManagerDashboardService.get_managed_groups(user).filter(
                parent__isnull=False,
                parent__parent__isnull=False,
            )
        )
        context["student_groups"] = (
            ScientificManagerDashboardService.get_student_groups_summary(user)
        )

        # محاسبه درآمد کل
        from django.db.models import Sum
        from apps.assessments.models import PaymentRequest
        
        managed_groups = ScientificManagerDashboardService.get_managed_groups(user)
        context["total_revenue"] = PaymentRequest.objects.filter(
            assessment__scientific_group__in=managed_groups,
            status="approved",
        ).aggregate(total=Sum("amount"))["total"] or 0

        return context