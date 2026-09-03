from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from apps.accounts.mixins import AdminOrScientificManagerRequiredMixin
from apps.assessments.models import Assessment, AssessmentRule, LearningObjective, Question, ScientificGroup


class AssessmentRuleCreateView(AdminOrScientificManagerRequiredMixin, View):
    """افزودن قوانین سوال به آزمون"""

    template_name = "dashboard/assessment_rule_create.html"

    def get(self, request, assessment_id):
        assessment = get_object_or_404(Assessment, id=assessment_id)

        # موضوع‌های گروه علمی
        if assessment.scientific_group:
            topics = ScientificGroup.objects.filter(
                parent=assessment.scientific_group,
                is_active=True,
            )
            if not topics.exists():
                topics = ScientificGroup.objects.filter(id=assessment.scientific_group.id)
        else:
            topics = ScientificGroup.objects.none()

        objectives = LearningObjective.objects.filter(
            scientific_group__in=topics,
            is_active=True,
        )

        existing_rules = assessment.rules.all()

        return render(request, self.template_name, {
            "assessment": assessment,
            "topics": topics,
            "objectives": objectives,
            "existing_rules": existing_rules,
            "difficulty_choices": Question.Difficulty.choices,
        })

    def post(self, request, assessment_id):
        assessment = get_object_or_404(Assessment, id=assessment_id)

        objective_id = request.POST.get("learning_objective")
        difficulty = request.POST.get("difficulty")
        question_count = request.POST.get("question_count")

        if not objective_id:
            messages.error(request, "هدف آموزشی باید انتخاب شود.")
            return redirect("accounts:scientific_manager:scientific-manager-assessment-rule-create", assessment_id=assessment.id)

        rule = AssessmentRule(
            assessment=assessment,
            learning_objective_id=objective_id,
            difficulty=difficulty if difficulty else None,
            question_count=int(question_count or 1),
        )
        rule.save()
        messages.success(request, "قانون اضافه شد.")

        return redirect("accounts:scientific_manager:scientific-manager-assessment-rule-create", assessment_id=assessment.id)