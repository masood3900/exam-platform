from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.assessments.forms.discount_code_create_form import DiscountCodeCreateForm
from apps.assessments.models import DiscountCode


class AdminDiscountCodesView(LoginRequiredMixin, View):
    """مدیریت کدهای تخفیف"""

    template_name = "dashboard/admin/discount_codes.html"

    def get(self, request):
        codes = DiscountCode.objects.select_related(
            "assessment",
            "created_by",
        ).order_by("-created_at")

        form = DiscountCodeCreateForm()

        return render(request, self.template_name, {
            "codes": codes,
            "form": form,
        })

    def post(self, request):
        form = DiscountCodeCreateForm(request.POST)

        if form.is_valid():
            code = form.save(commit=False)
            code.created_by = request.user
            code.save()
            messages.success(request, f"کد تخفیف «{code.code}» ساخته شد.")
            return redirect("accounts:admin-discount-codes")

        codes = DiscountCode.objects.select_related(
            "assessment",
            "created_by",
        ).order_by("-created_at")

        return render(request, self.template_name, {
            "codes": codes,
            "form": form,
        })


class AdminDiscountCodeDeleteView(LoginRequiredMixin, View):
    """حذف کد تخفیف"""

    def post(self, request, code_id):
        code = get_object_or_404(DiscountCode, id=code_id)
        code_str = code.code
        code.delete()
        messages.success(request, f"کد تخفیف «{code_str}» حذف شد.")
        return redirect("accounts:admin-discount-codes")


class AdminDiscountCodeToggleView(LoginRequiredMixin, View):
    """فعال/غیرفعال کردن کد تخفیف"""

    def post(self, request, code_id):
        code = get_object_or_404(DiscountCode, id=code_id)
        code.is_active = not code.is_active
        code.save(update_fields=["is_active"])

        status = "فعال" if code.is_active else "غیرفعال"
        messages.success(request, f"کد «{code.code}» {status} شد.")
        return redirect("accounts:admin-discount-codes")
