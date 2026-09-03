from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.accounts.models import User
from apps.assessments.models import ScientificGroup, ScientificGroupMembership


class UserChangeRoleView(LoginRequiredMixin, View):
    """تغییر نقش کاربر"""

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        role = request.POST.get("role")
        group_id = request.POST.get("scientific_group")
        
        if not role or not group_id:
            messages.error(request, "نقش و گروه را انتخاب کنید.")
            return redirect("accounts:admin-user-directory")
        
        group = get_object_or_404(ScientificGroup, id=group_id)
        
        # غیرفعال کردن نقش قبلی
        ScientificGroupMembership.objects.filter(
            user=user,
            scientific_group=group,
            is_active=True,
        ).update(is_active=False)
        
        # ساخت نقش جدید
        membership, created = ScientificGroupMembership.objects.get_or_create(
            user=user,
            scientific_group=group,
            role=role,
            defaults={"is_active": True},
        )
        if not created:
            membership.is_active = True
            membership.save()
        
        messages.success(request, f"نقش {user.get_full_name()} تغییر کرد.")
        return redirect("accounts:admin-user-directory")