from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.assessments.models import Question


class QuestionStatusChangeView(LoginRequiredMixin, View):
    """تغییر وضعیت سوال توسط مدیر علمی"""

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        new_status = request.POST.get("status")
        
        valid_statuses = ["draft", "pending", "approved", "rejected"]
        
        if new_status in valid_statuses:
            question.status = new_status
            question.is_active = (new_status == "approved")
            question.save()
            
            messages.success(
                request, 
                f"سوال «{question.code}» به وضعیت «{question.get_status_display()}» تغییر کرد."
            )
        else:
            messages.error(request, "وضعیت نامعتبر است.")
        
        return redirect("accounts:scientific_manager:dashboard")