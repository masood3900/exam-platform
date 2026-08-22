from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from apps.assessments.models import Attempt


class AttemptHistoryView(LoginRequiredMixin,ListView):
    model = Attempt
    template_name = (
        "assessments/attempt/history.html"
    )
    context_object_name = "attempts"

    paginate_by = 10

    def get_queryset(self):
        return (
            Attempt.objects.filter(
                student=self.request.user,
                status=Attempt.Status.GRADED,
            )
            .select_related(
                "assessment",
                "assessment__course",
            )
            .order_by(
                "-finished_at",
            )
        )
