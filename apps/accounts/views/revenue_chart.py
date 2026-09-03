import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

from apps.assessments.models import Assessment, PaymentRequest, ScientificGroup
from apps.accounts.services.role_service import RoleService


class RevenueChartView(LoginRequiredMixin, TemplateView):
    """نمودار درآمد برای همه نقش‌ها"""

    template_name = "dashboard/components/revenue_chart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # تعیین محدوده بر اساس نقش
        from apps.assessments.models import LearningPath
        
        chart_type = self.request.GET.get("type", "auto")

        if chart_type == "financial" or (chart_type == "auto" and (user.is_staff or user.is_superuser)):
            # ادمین → همه حوزه‌ها (مثل مدیر مالی)
            items = ScientificGroup.objects.filter(
                parent=None,
                is_active=True,
            ).exclude(code__in=["SCI"])
            item_type = "domain"
        elif chart_type == "financial" or RoleService.is_financial_manager(user):
            # مدیر مالی → همه حوزه‌ها
            items = ScientificGroup.objects.filter(parent=None, is_active=True).exclude(code__in=["SCI"])
            item_type = "domain"
        elif chart_type == "domain" or RoleService.is_domain_manager(user):
            # مدیر کل → مسیرهای حوزه خودش
            from apps.accounts.services.domain_manager_dashboard_service import DomainManagerDashboardService
            domains = DomainManagerDashboardService.get_domains(user)
            fields = ScientificGroup.objects.filter(parent__in=domains)
            items = LearningPath.objects.filter(scientific_group__in=fields)
            item_type = "path"
        elif chart_type == "scientific" or RoleService.is_scientific_manager(user):
            # مدیر علمی → آزمون‌های خودش
            from apps.accounts.services.scientific_manager_dashboard_service import ScientificManagerDashboardService
            groups = ScientificManagerDashboardService.get_managed_groups(user)
            items = Assessment.objects.filter(scientific_group__in=groups)
            item_type = "assessment"
        else:
            items = []
            item_type = "none"

        labels = []
        values = []

        for item in items:
            if item_type == "domain":
                # درآمد همه آزمون‌های این حوزه
                fields = ScientificGroup.objects.filter(parent=item)
                topics = ScientificGroup.objects.filter(parent__in=fields)
                all_groups = list(fields) + list(topics)
                domain_assessments = Assessment.objects.filter(scientific_group__in=all_groups)
                revenue = PaymentRequest.objects.filter(
                    assessment__in=domain_assessments,
                    status="approved",
                ).aggregate(total=Sum("amount"))["total"] or 0
                labels.append(item.name)
            elif item_type == "path":
                # درآمد همه آزمون‌های این مسیر
                path_assessments = Assessment.objects.filter(
                    scientific_group=item.scientific_group,
                )
                revenue = PaymentRequest.objects.filter(
                    assessment__in=path_assessments,
                    status="approved",
                ).aggregate(total=Sum("amount"))["total"] or 0
                labels.append(item.name)
            else:
                revenue = PaymentRequest.objects.filter(
                    assessment=item,
                    status="approved",
                ).aggregate(total=Sum("amount"))["total"] or 0
                labels.append(item.title)

            values.append(revenue)

        context["labels"] = json.dumps(labels, ensure_ascii=False)
        context["values"] = json.dumps(values)
        context["total_revenue"] = sum(values)
        context["item_type"] = item_type

        return context
