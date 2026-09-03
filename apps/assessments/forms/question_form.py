from django import forms
from apps.assessments.models import Question, Choice, ScientificGroup, LearningObjective


class QuestionForm(forms.ModelForm):
    """فرم طراحی سوال جدید"""

    topic = forms.ModelChoiceField(
        queryset=ScientificGroup.objects.filter(is_active=True),
        label="دوره/موضوع",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    learning_objective = forms.ModelChoiceField(
        queryset=LearningObjective.objects.filter(is_active=True),
        label="هدف آموزشی",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Question
        fields = [
            "title",
            "body",
            "question_type",
            "difficulty",
            "score",
            "estimated_seconds",
            "explanation",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 4, "style": "direction: rtl; text-align: right;"}),
            "question_type": forms.Select(attrs={"class": "form-control"}),
            "difficulty": forms.Select(attrs={"class": "form-control"}),
            "score": forms.NumberInput(attrs={"class": "form-control"}),
            "estimated_seconds": forms.NumberInput(attrs={"class": "form-control"}),
            "explanation": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            from apps.accounts.services.question_designer_dashboard_service import QuestionDesignerDashboardService

            # فقط موضوع‌هایی که طراح بهشون تخصیص داره
            topics = QuestionDesignerDashboardService.get_designer_groups(self.user)
            self.fields["topic"].queryset = topics

            # فقط اهداف همون موضوع‌ها
            self.fields["learning_objective"].queryset = LearningObjective.objects.filter(
                scientific_group__in=topics,
                is_active=True,
            )

class ChoiceForm(forms.ModelForm):
    """فرم گزینه سوال"""

    class Meta:
        model = Choice
        fields = ["text", "is_correct", "explanation"]
        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control choice-text",
                "rows": 2,
                "placeholder": "متن گزینه را وارد کنید...",
                "style": "direction: rtl; text-align: right;",
            }),
            "is_correct": forms.CheckboxInput(attrs={
                "class": "form-check-input choice-correct",
            }),
            "explanation": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "توضیح این گزینه (اختیاری)",
            }),
        }


ChoiceFormSet = forms.inlineformset_factory(
    Question,
    Choice,
    form=ChoiceForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True,
)
