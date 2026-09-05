from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.assessments.models import Question


class QuestionDeleteView(LoginRequiredMixin, View):
    """حذف سوال"""

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)

        # همه سوالات قابل حذف هستن (حتی تایید شده)
        question.delete()
        messages.success(request, "سوال حذف شد.")

        return redirect("accounts:question_designer:dashboard")
