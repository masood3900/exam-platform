from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.models import ScientificGroup, LearningObjective, ScientificGroupMembership, Question


class AdminScientificGroupDeleteView(AdminRequiredMixin, View):
    """حذف حوزه"""

    def post(self, request, group_id):
        group = get_object_or_404(ScientificGroup, id=group_id)
        
        # چک زیرمجموعه
        if group.children.exists():
            messages.error(request, f"«{group.name}» زیرمجموعه دارد. اول زیرمجموعه‌ها را حذف کنید.")
            return redirect("accounts:admin-scientific-groups")
        
        group_name = group.name
        
        # پاک کردن وابسته‌ها
        LearningObjective.objects.filter(scientific_group=group).delete()
        Question.objects.filter(scientific_group=group).delete()
        ScientificGroupMembership.objects.filter(scientific_group=group).delete()
        
        # پاک کردن خودش
        group.delete()
        
        messages.success(request, f"حوزه «{group_name}» حذف شد.")
        return redirect("accounts:admin-scientific-groups")