from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.accounts.models import User
from apps.assessments.models import ScientificGroup, ScientificGroupMembership


class AssignDesignerView(LoginRequiredMixin, View):
    """افزودن طراح سوال توسط مدیر علمی"""

    def post(self, request):
        user_id = request.POST.get("user_id")
        group_id = request.POST.get("scientific_group_id")

        if not group_id:
            messages.error(request, "موضوع/دوره را انتخاب کنید.")
            return redirect("accounts:scientific_manager:dashboard")

        user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(ScientificGroup, id=group_id)

        membership, created = ScientificGroupMembership.objects.get_or_create(
            user=user,
            scientific_group=group,
            role=ScientificGroupMembership.Role.QUESTION_DESIGNER,
            defaults={"is_active": True},
        )
        
        if not created:
            membership.is_active = True
            membership.save()

        messages.success(request, f"{user.get_full_name()} به عنوان طراح سوال اضافه شد.")
        return redirect("accounts:scientific_manager:dashboard")