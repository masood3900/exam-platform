from django import forms

from apps.assessments.models import (
    Assessment,
    ScientificGroup,
    Course,
)


class AssessmentForm(forms.ModelForm):
    """فرم ساخت آزمون"""

    is_independent = forms.BooleanField(
        label="آزمون مستقل (پولی)",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    source_courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.filter(is_active=True, parent__isnull=False),
        label="دوره‌های منبع سوالات",
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control", "size": "5"}),
    )

    class Meta:
        model = Assessment
        fields = [
            "title",
            "assessment_type",
            "description",
            "price",
            "discount_percent",
            "duration_minutes",
            "passing_score",
            "max_attempts",
            "demo_attempts",
            "shuffle_questions",
            "shuffle_choices",
            "show_result_immediately",
            "scientific_group",
            "course",
            "is_public",
            "learning_path",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "assessment_type": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "price": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "discount_percent": forms.NumberInput(attrs={"class": "form-control", "min": "0", "max": "100"}),
            "duration_minutes": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "passing_score": forms.NumberInput(attrs={"class": "form-control", "min": "0", "max": "100"}),
            "max_attempts": forms.NumberInput(attrs={"class": "form-control", "min": "1", "value": "1"}),
            "demo_attempts": forms.NumberInput(attrs={"class": "form-control", "min": "0", "value": "1"}),
            "scientific_group": forms.Select(attrs={"class": "form-control"}),
            "course": forms.Select(attrs={"class": "form-control"}),
            "learning_path": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["scientific_group"].required = False
        self.fields["course"].required = False
        self.fields["source_courses"].required = False
        self.fields["learning_path"].required = False
        self.fields["max_attempts"].required = False
        self.fields["max_attempts"].initial = 1
        self.fields["demo_attempts"].initial = 1

        for field_name in ["shuffle_questions", "shuffle_choices", "show_result_immediately", "is_public", "is_independent"]:
            self.fields[field_name].widget.attrs["class"] = "form-check-input"

        if self.user:
            from apps.accounts.services.role_service import RoleService

            if RoleService.is_scientific_manager(self.user) and not RoleService.is_staff(self.user):
                from apps.accounts.services.scientific_manager_dashboard_service import (
                    ScientificManagerDashboardService,
                )
                groups = ScientificManagerDashboardService.get_managed_groups(self.user)
                self.fields["scientific_group"].queryset = groups
                self.fields["course"].queryset = Course.objects.filter(
                    scientific_group__in=groups,
                    is_active=True,
                    parent__isnull=False,
                )
                self.fields["source_courses"].queryset = Course.objects.filter(
                    scientific_group__in=groups,
                    is_active=True,
                    parent__isnull=False,
                )

    def clean(self):
        cleaned_data = super().clean()
        is_independent = cleaned_data.get("is_independent")
        course = cleaned_data.get("course")
        scientific_group = cleaned_data.get("scientific_group")
        price = cleaned_data.get("price")
        source_courses = cleaned_data.get("source_courses")

        if is_independent:
            if not scientific_group:
                raise forms.ValidationError("آزمون مستقل باید گروه علمی داشته باشد.")
            cleaned_data["course"] = None
            cleaned_data["learning_path"] = None
            if not price or price <= 0:
                raise forms.ValidationError("آزمون مستقل باید قیمت داشته باشد.")
        else:
            if not course:
                raise forms.ValidationError("آزمون وابسته باید دوره داشته باشد.")
            cleaned_data["price"] = 0
            cleaned_data["discount_percent"] = 0
            if course.scientific_group:
                cleaned_data["scientific_group"] = course.scientific_group
            if course.learning_path:
                cleaned_data["learning_path"] = course.learning_path
            cleaned_data["source_courses"] = []

        return cleaned_data