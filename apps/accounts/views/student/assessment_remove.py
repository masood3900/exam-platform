from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.assessments.models import AssessmentEnrollment


class AssessmentRemoveView(LoginRequiredMixin, View):
    """حذف آزمون از داشبورد دانشجو"""

    def post(self, request, enrollment_id):
        enrollment = get_object_or_404(
            AssessmentEnrollment,
            id=enrollment_id,
            user=request.user,
        )
        
        title = enrollment.assessment.title
        enrollment.delete()
        
        messages.success(request, f"آزمون «{title}» از داشبورد شما حذف شد.")
        from apps.accounts.services.role_service import RoleService
        if RoleService.is_student(request.user):
            return redirect("accounts:dashboard")
        return redirect("core:home")