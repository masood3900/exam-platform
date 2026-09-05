from django import forms
from apps.assessments.models import DiscountCode, Assessment


class DiscountCodeCreateForm(forms.ModelForm):
    """فرم ساخت کد تخفیف جدید"""

    class Meta:
        model = DiscountCode
        fields = [
            "code",
            "discount_percent",
            "assessment",
            "valid_from",
            "valid_until",
            "max_uses",
            "is_active",
        ]
        widgets = {
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "مثلاً: WELCOME10",
            }),
            "discount_percent": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
                "max": 100,
            }),
            "assessment": forms.Select(attrs={
                "class": "form-control",
            }),
            "valid_from": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),
            "valid_until": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),
            "max_uses": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assessment"].queryset = Assessment.objects.all()
        self.fields["assessment"].required = False
        self.fields["valid_from"].required = False
        self.fields["valid_until"].required = False
