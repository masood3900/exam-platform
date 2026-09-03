from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.assessments.models import Assessment


class AssessmentToggleActiveView(LoginRequiredMixin, View):
    """فعال/غیرفعال کردن آزمون"""

    def post(self, request, assessment_id):
        assessment = get_object_or_404(Assessment, id=assessment_id)
        
        assessment.is_active = not assessment.is_active
        assessment.save()
        
        status = "فعال" if assessment.is_active else "غیرفعال"
        messages.success(request, f"آزمون «{assessment.title}» {status} شد.")
        return redirect("accounts:scientific_manager:dashboard")