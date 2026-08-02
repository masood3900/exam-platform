from django import forms
from apps.assessments.models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "title",
            "body",
            "learning_objective",
            "difficulty",
            "question_type",
            "score",
            "estimated_seconds",
            "explanation",
        ]
        widgets = {
            "body":forms.Textarea(
                attrs={"rows":4}
            ),

        }




        
