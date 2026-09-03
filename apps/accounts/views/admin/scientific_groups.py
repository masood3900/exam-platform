from django.views.generic import TemplateView

from apps.accounts.mixins import AdminRequiredMixin
from apps.accounts.models import User
from apps.assessments.models import ScientificGroup


class AdminScientificGroupListView(AdminRequiredMixin, TemplateView):
    """لیست حوزه‌های علمی"""

    template_name = "dashboard/admin/scientific_groups.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["domains"] = ScientificGroup.objects.filter(
            parent=None,
        ).prefetch_related("memberships__user")
        
        context["fields"] = ScientificGroup.objects.filter(
            parent__isnull=False,
        ).select_related("parent")
        
        context["all_users"] = User.objects.filter(is_active=True)
        
        return context