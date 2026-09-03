from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.accounts.models import User


class UserDeleteView(LoginRequiredMixin, View):
    """غیرفعال کردن کاربر (به جای حذف)"""

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        if user.id == request.user.id:
            messages.error(request, "نمی‌توانید خودتان را غیرفعال کنید.")
            return redirect("accounts:admin-user-directory")
        
        user.is_active = False
        user.save()
        
        messages.success(request, f"کاربر «{user.get_full_name()}» غیرفعال شد.")
        return redirect("accounts:admin-user-directory")