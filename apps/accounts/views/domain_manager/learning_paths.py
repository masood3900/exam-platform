from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.accounts.models import User
from apps.assessments.models import LearningPath, ScientificGroupMembership, ScientificGroup


class DomainManagerLearningPathListView(LoginRequiredMixin, ListView):
    """لیست مسیرهای آموزشی برای مدیر کل"""

    model = LearningPath
    template_name = "dashboard/domain_manager/learning_paths.html"
    context_object_name = "learning_paths"

    def get_queryset(self):
        domain_ids = ScientificGroupMembership.objects.filter(
            user=self.request.user,
            role=ScientificGroupMembership.Role.DOMAIN_MANAGER,
            is_active=True,
        ).values_list("scientific_group_id", flat=True)

        field_ids = ScientificGroup.objects.filter(
            parent_id__in=domain_ids,
        ).values_list("id", flat=True)

        return LearningPath.objects.filter(
            scientific_group_id__in=field_ids,
        ).prefetch_related(
            "scientific_group__memberships__user",
            "prerequisites",
        ).order_by("order", "name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_users"] = User.objects.filter(is_active=True)
        return context