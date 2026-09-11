from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from apps.accounts.mixins import AdminRequiredMixin

User = get_user_model()


class AdminChangePasswordView(AdminRequiredMixin, View):
    """تغییر پسورد کاربر توسط ادمین"""

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not new_password or not confirm_password:
            messages.error(request, "هر دو فیلد الزامی است.")
            return redirect("accounts:user-management")

        if new_password != confirm_password:
            messages.error(request, "رمز عبور و تکرار آن مطابقت ندارند.")
            return redirect("accounts:user-management")

        if len(new_password) < 8:
            messages.error(request, "رمز عبور حداقل ۸ کاراکتر باشد.")
            return redirect("accounts:user-management")

        user.password = make_password(new_password)
        user.save()

        messages.success(request, f"رمز عبور «{user.username}» تغییر کرد.")
        return redirect("accounts:user-management")
