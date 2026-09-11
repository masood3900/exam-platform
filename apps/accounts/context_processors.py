from apps.accounts.services.role_service import (
    RoleService,
)
from apps.assessments.models import ScientificGroup


def dashboard_context(request):
    context = {
        "dashboard_url": None,
        "available_dashboards": [],
        "categories": [],
    }

    # حوزه‌های آموزشی برای همه
    context["categories"] = ScientificGroup.objects.filter(
        parent__isnull=True,
        is_active=True,
    ).exclude(
        name__icontains="فنی"
    ).prefetch_related("children")

    if not request.user.is_authenticated:
        return context

    context["dashboard_url"] = RoleService.get_dashboard_url(request.user)
    context["available_dashboards"] = RoleService.get_available_dashboards(request.user)

    return context
