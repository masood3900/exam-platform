import uuid
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.assessments.forms.question_form import (
    QuestionForm,
    ChoiceFormSet,
)
from apps.assessments.models import Question


class QuestionCreateView(LoginRequiredMixin, View):
    """ساخت سوال جدید با گزینه‌ها"""

    template_name = "dashboard/question_designer/question_create.html"

    def get(self, request):
        form = QuestionForm(user=request.user)
        formset = ChoiceFormSet(prefix="choices")
        return render(request, self.template_name, {
            "form": form,
            "formset": formset,
        })

    def post(self, request):
        form = QuestionForm(request.POST, user=request.user)
        formset = ChoiceFormSet(request.POST, prefix="choices")

        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.code = f"Q-{uuid.uuid4().hex[:8].upper()}"
            question.status = Question.QuestionStatus.DRAFT
            question.scientific_group = form.cleaned_data["topic"]
            question.learning_objective = form.cleaned_data["learning_objective"]
            question.save()

            formset.instance = question
            choices = formset.save(commit=False)

            for obj in formset.deleted_objects:
                obj.delete()

            order = 1
            for choice in choices:
                if choice.text:
                    choice.order = order
                    choice.save()
                    order += 1

            messages.success(request, "سوال با موفقیت به عنوان پیش‌نویس ذخیره شد.")
            return redirect("accounts:question_designer:dashboard")

        return render(request, self.template_name, {
            "form": form,
            "formset": formset,
        })