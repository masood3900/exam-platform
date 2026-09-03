from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.accounts.models import User
from apps.assessments.models import Assessment
from apps.accounts.services.user_role_transition_service import UserRoleTransitionService


class AssessmentAddStudentView(LoginRequiredMixin, View):
    """افزودن دانشجو به آزمون"""

    def post(self, request, assessment_id):
        assessment = get_object_or_404(Assessment, id=assessment_id)
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)
        
        try:
            UserRoleTransitionService.manager_add_student_to_assessment(user, assessment)
            messages.success(request, f"{user.get_full_name()} به «{assessment.title}» اضافه شد.")
        except ValueError as e:
            messages.error(request, str(e))
        
        return redirect("accounts:scientific_manager:dashboard")