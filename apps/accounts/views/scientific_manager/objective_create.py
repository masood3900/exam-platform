from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.accounts.services.scientific_group_service import ScientificGroupService


class ObjectiveCreateView(LoginRequiredMixin, View):
    """ساخت هدف آموزشی توسط مدیر علمی"""

    template_name = "dashboard/scientific_manager/objective_create.html"

    def get(self, request):
        # موضوع‌هایی که مدیر علمی ساخته
        fields = ScientificGroupService.get_manager_fields(request.user)
        topics = []
        for field in fields:
            topics.extend(ScientificGroupService.get_topics_of_field(field.id))
        
        return render(request, self.template_name, {"topics": topics})

    def post(self, request):
        name = request.POST.get("name")
        code = request.POST.get("code")
        description = request.POST.get("description", "")
        topic_id = request.POST.get("scientific_group")
        
        if not name or not code or not topic_id:
            messages.error(request, "همه فیلدها الزامی است.")
            return redirect("accounts:scientific_manager:objective-create")
        
        objective = ScientificGroupService.create_objective(name, code, description, topic_id)
        
        messages.success(request, f"هدف «{objective.name}» ساخته شد.")
        return redirect("accounts:scientific_manager:dashboard")