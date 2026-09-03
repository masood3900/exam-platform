from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.assessments.models import Question, QuestionReviewHistory


class QuestionSubmitView(LoginRequiredMixin, View):
    """ارسال سوال برای تایید توسط طراح"""

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        note = request.POST.get("note", "")
        
        # تغییر وضعیت سوال
        question.status = Question.QuestionStatus.PENDING
        question.save()
        
        # ثبت در تاریخچه
        QuestionReviewHistory.objects.create(
            question=question,
            reviewer=request.user,
            action=QuestionReviewHistory.Action.SUBMIT,
            note=note,
        )
        
        messages.success(
            request,
            f"سوال «{question.code}» برای تایید مدیر علمی ارسال شد.",
        )
        
        return redirect("accounts:question_designer:dashboard")