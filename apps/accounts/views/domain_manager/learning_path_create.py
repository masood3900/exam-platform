from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.assessments.models import LearningPath, ScientificGroup, ScientificGroupMembership


class DomainManagerLearningPathCreateView(LoginRequiredMixin, View):
    """ساخت مسیر آموزشی توسط مدیر کل"""

    template_name = "dashboard/domain_manager/learning_path_create.html"

    def get(self, request):
        domains = ScientificGroup.objects.filter(
            memberships__user=request.user,
            memberships__role=ScientificGroupMembership.Role.DOMAIN_MANAGER,
            memberships__is_active=True,
            parent=None,
        )
        return render(request, self.template_name, {"domains": domains})

    def post(self, request):
        name = request.POST.get("name")
        slug = request.POST.get("slug")
        description = request.POST.get("description", "")
        icon = request.POST.get("icon", "")
        color = request.POST.get("color", "primary")
        order = request.POST.get("order", 0)
        domain_id = request.POST.get("scientific_group")
        
        if not name or not slug:
            messages.error(request, "نام و شناسه الزامی است.")
            return redirect("accounts:domain_manager:learning-path-create")
        
        domain = ScientificGroup.objects.get(id=domain_id)
        
        # ساخت رشته جدید برای این مسیر
        field = ScientificGroup.objects.create(
            name=name,
            code=slug.upper(),
            parent=domain,
        )
        
        # ساخت مسیر
        LearningPath.objects.create(
            name=name,
            slug=slug,
            description=description,
            icon=icon,
            color=color,
            order=order,
            scientific_group=field,  # ← رشته
        )
        
        messages.success(request, f"مسیر «{name}» ساخته شد.")
        return redirect("accounts:domain_manager:learning-paths")