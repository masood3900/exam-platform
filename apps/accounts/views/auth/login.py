from django.contrib.auth.views import LoginView

from apps.accounts.services.role_service import (
    RoleService,
)


class UserLoginView(LoginView):

    template_name = (
        "accounts/login.html"
    )

    def get_success_url(self):

        return RoleService.get_dashboard_url(
            self.request.user
        )