from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.assessments.models import LearningPath


class DomainManagerLearningPathDeleteView(LoginRequiredMixin, View):
    """حذف مسیر توسط مدیر کل"""

    def post(self, request, path_id):
        path = get_object_or_404(LearningPath, id=path_id)
        
        path_name = path.name
        path.delete()
        
        messages.success(request, f"مسیر «{path_name}» حذف شد.")
        return redirect("accounts:domain_manager:dashboard")
