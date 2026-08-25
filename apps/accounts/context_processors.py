from apps.accounts.services.role_service import (
    RoleService,
)


def dashboard_context(request):

    if not request.user.is_authenticated:

        return {
            "dashboard_url": None,
        }

    return {
        "dashboard_url":
            RoleService.get_dashboard_url(
                request.user,
            ),
    }