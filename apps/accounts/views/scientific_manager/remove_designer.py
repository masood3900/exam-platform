from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.assessments.models import ScientificGroupMembership


class RemoveDesignerView(LoginRequiredMixin, View):
    """حذف طراح سوال توسط مدیر علمی"""

    def post(self, request, membership_id):
        membership = get_object_or_404(ScientificGroupMembership, id=membership_id)
        
        membership.is_active = False
        membership.save()
        
        messages.success(request, f"{membership.user.get_full_name()} از طراحان حذف شد.")
        return redirect("accounts:scientific_manager:dashboard")