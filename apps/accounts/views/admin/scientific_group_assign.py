from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.accounts.mixins import AdminRequiredMixin
from apps.accounts.models import User
from apps.assessments.models import ScientificGroup, ScientificGroupMembership


class AdminScientificGroupAssignView(AdminRequiredMixin, View):
    """اختصاص کاربر به حوزه"""

    def post(self, request, group_id):
        group = get_object_or_404(ScientificGroup, id=group_id)
        user_id = request.POST.get("user_id")
        role = request.POST.get("role")
        
        user = get_object_or_404(User, id=user_id)
        
        # برای مدیر کل و مدیر علمی - اگه قبلاً داره، جایگزین کن
        if role in ["domain_manager", "scientific_manager"]:
            # غیرفعال کردن قبلی
            ScientificGroupMembership.objects.filter(
                scientific_group=group,
                role=role,
                is_active=True,
            ).update(is_active=False)
        
        # ساخت یا فعال‌سازی جدید
        membership, created = ScientificGroupMembership.objects.get_or_create(
            user=user,
            scientific_group=group,
            role=role,
            defaults={"is_active": True},
        )
        
        if not created:
            membership.is_active = True
            membership.save()
        
        messages.success(request, f"{user.get_full_name()} به {group.name} اضافه شد.")
        return redirect("accounts:admin-scientific-groups")