import uuid
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from apps.accounts.mixins import AdminOrScientificManagerRequiredMixin
from apps.assessments.forms.assessment_form import AssessmentForm
from apps.assessments.services.assessment_enrollment_service import AssessmentEnrollmentService


class AssessmentCreateView(AdminOrScientificManagerRequiredMixin, View):
    """ساخت آزمون جدید"""

    template_name = "dashboard/assessment_create.html"

    def get(self, request):
        form = AssessmentForm(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AssessmentForm(request.POST, user=request.user)

        if form.is_valid():
            assessment = AssessmentEnrollmentService.create_assessment(
                title=form.cleaned_data["title"],
                assessment_type=form.cleaned_data["assessment_type"],
                description=form.cleaned_data.get("description", ""),
                price=form.cleaned_data.get("price", 0),
                discount_percent=form.cleaned_data.get("discount_percent", 0),
                duration_minutes=form.cleaned_data.get("duration_minutes", 30),
                passing_score=form.cleaned_data.get("passing_score", 70),
                max_attempts=form.cleaned_data.get("max_attempts") or 1,
                demo_attempts=form.cleaned_data.get("demo_attempts", 1),
                scientific_group=form.cleaned_data.get("scientific_group"),
                course=form.cleaned_data.get("course"),
                is_public=form.cleaned_data.get("is_public", False),
                created_by=request.user,
                source_courses=form.cleaned_data.get("source_courses", []),
            )

            messages.success(request, f"آزمون «{assessment.title}» با موفقیت ایجاد شد.")
            return redirect("accounts:admin-assessment-rule-create", assessment_id=assessment.id)

        return render(request, self.template_name, {"form": form})