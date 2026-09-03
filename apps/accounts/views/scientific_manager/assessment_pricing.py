from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.assessments.models import Assessment


class AssessmentPricingView(LoginRequiredMixin, View):
    """تغییر قیمت و تخفیف آزمون"""

    template_name = "dashboard/scientific_manager/assessment_pricing.html"

    def get(self, request, assessment_id):
        assessment = get_object_or_404(Assessment, id=assessment_id)
        return render(request, self.template_name, {"assessment": assessment})

    def post(self, request, assessment_id):
        assessment = get_object_or_404(Assessment, id=assessment_id)

        price = request.POST.get("price", 0)
        discount = request.POST.get("discount_percent", 0)

        assessment.price = int(price or 0)
        assessment.discount_percent = int(discount or 0)
        assessment.save()

        messages.success(request, f"قیمت «{assessment.title}» به‌روزرسانی شد.")
        return redirect("accounts:scientific_manager:dashboard")
