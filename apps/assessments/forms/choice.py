from django import forms
from apps.assessments.models import Choice



class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = [
            "text",
            "is_correct",
            "explanation",
        ]
        widgets = {
            "text":forms.Textarea(
                attrs={"rows":2}
            ),
            "explanation":forms.Textarea(
                attrs={"rows":2}
            ),
        }