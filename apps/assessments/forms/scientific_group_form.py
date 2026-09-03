from django import forms

from apps.assessments.models import ScientificGroup


class ScientificGroupForm(forms.ModelForm):
    """فرم ساخت حوزه"""

    class Meta:
        model = ScientificGroup
        fields = ["name", "code", "description", "parent"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "parent": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].required = False