from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from apps.accounts.models import User
from apps.assessments.models import Attempt


class StudentDetailView(LoginRequiredMixin, TemplateView):
    """جزئیات دانشجو"""

    template_name = "dashboard/scientific_manager/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs["student_id"]

        student = get_object_or_404(User, id=student_id)

        # همه تلاش‌های دانشجو
        attempts = Attempt.objects.filter(
            student=student,
            status="graded",
        ).select_related("assessment").order_by("-finished_at")

        # آخرین نتیجه
        last_attempt = attempts.first()

        # آمار
        stats = {
            "total": attempts.count(),
            "avg": round(attempts.aggregate(avg=Avg("percentage"))["avg"] or 0, 2),
            "passed": attempts.filter(passed=True).count(),
        }

        # آخرین نتیجه - objective report
        objective_report = []
        last_attempt_questions = []
        
        if last_attempt:
            from apps.assessments.services.analytics_service import AnalyticsService
            try:
                objective_report = AnalyticsService.learning_objective_report(last_attempt)
            except:
                pass
            
            last_attempt_questions = last_attempt.questions.select_related(
                "question",
            ).order_by("order")

        context["student"] = student
        context["attempts"] = attempts
        context["last_attempt"] = last_attempt
        context["stats"] = stats
        context["objective_report"] = objective_report
        context["last_attempt_questions"] = last_attempt_questions
        return context
