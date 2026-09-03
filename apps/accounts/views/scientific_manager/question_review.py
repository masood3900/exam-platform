from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.assessments.models import Question, QuestionReviewHistory


class QuestionReviewView(LoginRequiredMixin, View):
    """تایید یا رد سوال توسط مدیر علمی"""

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        action = request.POST.get("action")
        review_note = request.POST.get("review_note", "")
        
        if action == "approve":
            question.status = Question.QuestionStatus.APPROVED
            question.is_active = True
            question.reviewed_by = request.user
            question.review_note = review_note
            question.save()
            
            # ثبت در تاریخچه
            QuestionReviewHistory.objects.create(
                question=question,
                reviewer=request.user,
                action=QuestionReviewHistory.Action.APPROVE,
                note=review_note,
            )
            
            messages.success(request, f"سوال «{question.code}» تایید شد.")
        
        elif action == "reject":
            question.status = Question.QuestionStatus.REJECTED
            question.is_active = False
            question.reviewed_by = request.user
            question.review_note = review_note
            question.save()
            
            # ثبت در تاریخچه
            QuestionReviewHistory.objects.create(
                question=question,
                reviewer=request.user,
                action=QuestionReviewHistory.Action.REJECT,
                note=review_note,
            )
            
            messages.warning(request, f"سوال «{question.code}» رد شد.")
        
        elif action == "return":
            question.status = Question.QuestionStatus.REJECTED
            question.is_active = False
            question.reviewed_by = request.user
            question.review_note = review_note
            question.save()
            
            # ثبت در تاریخچه
            QuestionReviewHistory.objects.create(
                question=question,
                reviewer=request.user,
                action=QuestionReviewHistory.Action.RETURN,
                note=review_note,
            )
            
            messages.info(request, f"سوال «{question.code}» برای اصلاح برگشت داده شد.")
        
        return redirect("accounts:scientific_manager:dashboard")