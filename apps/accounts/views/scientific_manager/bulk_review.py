from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.accounts.services.question_service import QuestionService


class BulkReviewView(LoginRequiredMixin, View):
    """تایید/رد گروهی سوالات"""

    def post(self, request):
        question_ids = request.POST.getlist("question_ids")
        action = request.POST.get("action")
        note = request.POST.get("review_note", "")
        
        if not question_ids:
            messages.warning(request, "سوالی انتخاب نشده است.")
            return redirect("accounts:scientific_manager:dashboard")
        
        count = QuestionService.bulk_review(question_ids, request.user, action, note)
        
        if action == "approve":
            messages.success(request, f"{count} سوال تایید شد.")
        else:
            messages.warning(request, f"{count} سوال رد شد.")
        
        return redirect("accounts:scientific_manager:dashboard")