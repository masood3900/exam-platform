from django.views.generic import TemplateView

from apps.accounts.mixins import AdminRequiredMixin
from apps.accounts.services.user_directory_service import UserDirectoryService
from apps.assessments.models import ScientificGroup


class UserDirectoryView(AdminRequiredMixin, TemplateView):
    """دایرکتوری کاربران"""

    template_name = "dashboard/admin/user_directory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["directory_data"] = UserDirectoryService.get_directory_data()
        context["all_groups"] = ScientificGroup.objects.filter(is_active=True)
        return context