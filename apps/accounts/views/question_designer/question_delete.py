from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.assessments.models import Question


class QuestionDeleteView(LoginRequiredMixin, View):
    """حذف سوال"""

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        
        if question.status in [Question.QuestionStatus.DRAFT, Question.QuestionStatus.REJECTED]:
            question.delete()
            messages.success(request, "سوال حذف شد.")
        else:
            messages.error(request, "سوال تایید شده یا در انتظار تایید قابل حذف نیست.")
        
        return redirect("accounts:question_designer:dashboard")