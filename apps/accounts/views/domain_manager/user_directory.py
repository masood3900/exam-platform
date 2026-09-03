from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.accounts.services.user_directory_service import UserDirectoryService
from apps.accounts.services.role_service import RoleService


class DomainManagerUserDirectoryView(LoginRequiredMixin, TemplateView):
    """دایرکتوری کاربران برای مدیر کل"""

    template_name = "dashboard/domain_manager/user_directory.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        exclude_roles = []
        if RoleService.is_domain_manager(user):
            exclude_roles.append("domain_managers")

        context["directory_data"] = UserDirectoryService.get_directory_data(
            scope_user=user,
            exclude_roles=exclude_roles,
        )
        context["upper_manager"] = UserDirectoryService.get_upper_manager(user)
        return context