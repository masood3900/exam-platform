from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from apps.accounts.mixins import AdminRequiredMixin
from apps.assessments.forms.scientific_group_form import ScientificGroupForm


class AdminScientificGroupCreateView(AdminRequiredMixin, View):
    """ساخت حوزه جدید"""

    template_name = "dashboard/admin/scientific_group_create.html"

    def get(self, request):
        form = ScientificGroupForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ScientificGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"حوزه «{group.name}» ساخته شد.")
            return redirect("accounts:admin-scientific-groups")
        return render(request, self.template_name, {"form": form})