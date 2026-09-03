from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.accounts.services.domain_manager_dashboard_service import DomainManagerDashboardService
from apps.assessments.models import LearningPath, ScientificGroup, ScientificGroupMembership


class DomainManagerDashboardView(LoginRequiredMixin, TemplateView):
    """داشبورد مدیر کل"""

    template_name = "dashboard/domain_manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["stats"] = DomainManagerDashboardService.overall_stats(user)
        context["fields"] = DomainManagerDashboardService.get_fields(user)
        context["courses"] = DomainManagerDashboardService.get_courses(user)
        context["assessments"] = DomainManagerDashboardService.get_assessments(user)
        context["managers"] = DomainManagerDashboardService.get_managers(user)

        # حوزه‌های کاربر
        domain_ids = ScientificGroupMembership.objects.filter(
            user=user,
            role=ScientificGroupMembership.Role.DOMAIN_MANAGER,
            is_active=True,
        ).values_list("scientific_group_id", flat=True)

        # رشته‌های زیرمجموعه حوزه‌ها
        field_ids = ScientificGroup.objects.filter(
            parent_id__in=domain_ids,
        ).values_list("id", flat=True)

        # مسیرهای این رشته‌ها
        context["learning_paths"] = LearningPath.objects.filter(
            scientific_group_id__in=field_ids,
        ).prefetch_related("scientific_group__memberships__user")

        context["managed_domains"] = ScientificGroup.objects.filter(
            id__in=domain_ids,
        )

        from django.db.models import Sum
        from apps.assessments.models import PaymentRequest, Assessment
        
        # محاسبه درآمد کل حوزه
        fields = ScientificGroup.objects.filter(parent__in=domain_ids)
        topics = ScientificGroup.objects.filter(parent__in=fields)
        all_groups = list(fields) + list(topics)
        
        domain_assessments = Assessment.objects.filter(scientific_group__in=all_groups)
        context["total_revenue"] = PaymentRequest.objects.filter(
            assessment__in=domain_assessments,
            status="approved",
        ).aggregate(total=Sum("amount"))["total"] or 0

        return context