from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View


class ProfileChangePasswordView(LoginRequiredMixin, View):
    """تغییر رمز عبور از پروفایل"""

    template_name = "accounts/change_password.html"

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "✅ رمز عبور با موفقیت تغییر کرد.")
            return redirect("accounts:profile")
        else:
            messages.error(request, "❌ خطا در تغییر رمز. لطفاً دوباره تلاش کنید.")

        return render(request, self.template_name, {"form": form})
