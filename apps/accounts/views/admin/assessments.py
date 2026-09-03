from django.views.generic import ListView

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import Assessment


class AdminAssessmentListView(AdminRequiredMixin, ListView):
    """لیست آزمون‌ها"""

    model = Assessment
    template_name = "dashboard/admin/assessments.html"
    context_object_name = "assessments"
    paginate_by = 25

    def get_queryset(self):
        return Assessment.objects.all().select_related(
            "scientific_group",
            "course",
        ).order_by("-created_at")