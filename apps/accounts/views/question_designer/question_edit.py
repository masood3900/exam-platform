from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from apps.accounts.services.question_service import QuestionService
from apps.assessments.forms.question_form import QuestionForm, ChoiceFormSet
from apps.assessments.models import Question


class QuestionEditView(LoginRequiredMixin, View):
    """ویرایش سوال"""

    template_name = "dashboard/question_designer/question_create.html"

    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = QuestionForm(instance=question, user=request.user)
        formset = ChoiceFormSet(instance=question, prefix="choices")
        return render(request, self.template_name, {"form": form, "formset": formset})

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = QuestionForm(request.POST, instance=question, user=request.user)
        formset = ChoiceFormSet(request.POST, instance=question, prefix="choices")

        if form.is_valid() and formset.is_valid():
            QuestionService.update_question_with_choices(
                question=question,
                form=form,
                formset=formset,
            )

            messages.success(request, "سوال ویرایش شد.")
            return redirect("accounts:question_designer:dashboard")

        return render(request, self.template_name, {"form": form, "formset": formset})