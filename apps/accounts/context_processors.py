from apps.accounts.services.role_service import (
    RoleService,
)


def dashboard_context(request):

    if not request.user.is_authenticated:
        return {
            "dashboard_url": None,
            "available_dashboards": [],
        }

    return {
        "dashboard_url": RoleService.get_dashboard_url(request.user),
        "available_dashboards": RoleService.get_available_dashboards(request.user),
    }