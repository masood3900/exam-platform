from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.accounts.models import User
from apps.accounts.services.scientific_group_service import ScientificGroupService


class TopicCreateView(LoginRequiredMixin, View):
    """ساخت موضوع + اهداف + انتصاب طراحان"""

    template_name = "dashboard/scientific_manager/topic_create.html"

    def get(self, request):
        fields = ScientificGroupService.get_manager_fields(request.user)
        all_users = User.objects.filter(is_active=True)
        return render(request, self.template_name, {
            "fields": fields,
            "all_users": all_users,
        })

    def post(self, request):
        name = request.POST.get("name")
        code = request.POST.get("code")
        description = request.POST.get("description", "")
        parent_id = request.POST.get("parent")
        
        if not name or not code or not parent_id:
            messages.error(request, "همه فیلدها الزامی است.")
            return redirect("accounts:scientific_manager:topic-create")
        
        # جمع‌آوری اهداف
        objective_data_list = []
        obj_names = request.POST.getlist("objective_names[]")
        obj_codes = request.POST.getlist("objective_codes[]")
        
        for i in range(len(obj_names)):
            if obj_names[i].strip():
                objective_data_list.append({
                    "name": obj_names[i],
                    "code": obj_codes[i] if i < len(obj_codes) else "",
                })
        
        # طراحان
        designer_ids = request.POST.getlist("designer_ids[]")
        
        result = ScientificGroupService.create_topic_with_objectives_and_designers(
            name=name,
            code=code,
            description=description,
            parent_id=parent_id,
            objective_data_list=objective_data_list,
            designer_ids=designer_ids,
        )
        
        messages.success(
            request,
            f"موضوع «{result['topic'].name}» با {len(result['objectives'])} هدف و {len(result['designers'])} طراح ساخته شد."
        )
        return redirect("accounts:scientific_manager:dashboard")