from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.accounts.models import User
from apps.assessments.models import LearningPath, ScientificGroupMembership


class DomainManagerAssignManagerView(LoginRequiredMixin, View):
    """اختصاص مدیر علمی به مسیر"""

    def post(self, request, path_id):
        path = get_object_or_404(LearningPath, id=path_id)
        user_id = request.POST.get("user_id")
        
        user = get_object_or_404(User, id=user_id)
        
        # غیرفعال کردن مدیر علمی قبلی
        ScientificGroupMembership.objects.filter(
            scientific_group=path.scientific_group,
            role=ScientificGroupMembership.Role.SCIENTIFIC_MANAGER,
            is_active=True,
        ).update(is_active=False)
        
        # ساخت یا فعال‌سازی جدید
        membership, created = ScientificGroupMembership.objects.get_or_create(
            user=user,
            scientific_group=path.scientific_group,
            role=ScientificGroupMembership.Role.SCIENTIFIC_MANAGER,
            defaults={"is_active": True},
        )
        
        if not created:
            membership.is_active = True
            membership.save()
        
        messages.success(request, f"{user.get_full_name()} به عنوان مدیر علمی «{path.name}» منصوب شد.")
        return redirect("accounts:domain_manager:learning-paths")