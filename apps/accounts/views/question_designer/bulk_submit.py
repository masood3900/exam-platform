from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.accounts.services.question_service import QuestionService

class BulkSubmitView(LoginRequiredMixin, View):
    """ارسال گروهی سوالات"""
    def post(self, request):
        question_ids = request.POST.getlist("question_ids")
        if not question_ids:
            messages.warning(request,"سوالی انتخاب نشده است.")
            return redirect("accounts:question_designer:dashboard")

        count = QuestionService.bulk_submit(question_ids, request.user)
        messages.success(request, f"{count} سوال برای تایید ارسال شد.")
        return redirect("accounts:question_designer:dashboard")


        

