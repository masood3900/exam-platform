from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from apps.assessments.models import Assessment, AssessmentEnrollment, ScientificGroupMembership
from apps.accounts.services.user_directory_service import UserDirectoryService
from apps.messaging.services.direct_message_service import DirectMessageService


class ContactManagerView(LoginRequiredMixin, View):
    """ارتباط با مدیر علمی"""

    template_name = "dashboard/student/contact_manager.html"

    def get(self, request, assessment_id):
        assessment = get_object_or_404(Assessment, id=assessment_id)
        
        # چک کن کاربر ثبت‌نام کرده
        enrollment = AssessmentEnrollment.objects.filter(
            user=request.user,
            assessment=assessment,
        ).first()
        
        if not enrollment:
            messages.error(request, "شما در این آزمون ثبت‌نام نکرده‌اید.")
            return redirect("core:assessment-detail", assessment_id=assessment.id)
        
        # پیدا کردن مدیر علمی
        manager_membership = None
        if assessment.scientific_group:
            manager_membership = ScientificGroupMembership.objects.filter(
                scientific_group=assessment.scientific_group,
                role="scientific_manager",
                is_active=True,
            ).select_related("user").first()
            
            # اگه توی خود گروه نبود، توی والد بگرد
            if not manager_membership and assessment.scientific_group.parent:
                manager_membership = ScientificGroupMembership.objects.filter(
                    scientific_group=assessment.scientific_group.parent,
                    role="scientific_manager",
                    is_active=True,
                ).select_related("user").first()
        
        # گرفتن تاریخچه گفتگو
        conversation = []
        if manager_membership:
            conversation = DirectMessageService.get_conversation(
                request.user,
                manager_membership.user,
            )
        
        manager_data = None
        if manager_membership:
            manager_data = UserDirectoryService.get_user_card_data(
                manager_membership.user,
                role_label="مدیر علمی",
                role_color="info",
            )
        
        return render(request, self.template_name, {
            "assessment": assessment,
            "manager": manager_data,
            "manager_user": manager_membership.user if manager_membership else None,
            "conversation": conversation,
        })

    def post(self, request, assessment_id):
        assessment = get_object_or_404(Assessment, id=assessment_id)
        manager_user_id = request.POST.get("manager_user_id")
        text = request.POST.get("text", "")
        
        if not manager_user_id or not text.strip():
            messages.error(request, "پیام نمی‌تواند خالی باشد.")
            return redirect("accounts:contact-manager", assessment_id=assessment.id)
        
        from apps.accounts.models import User
        manager_user = get_object_or_404(User, id=manager_user_id)
        
        DirectMessageService.send_message(
            sender=request.user,
            receiver=manager_user,
            text=text,
        )
        
        messages.success(request, "پیام ارسال شد.")
        return redirect("accounts:contact-manager", assessment_id=assessment.id)