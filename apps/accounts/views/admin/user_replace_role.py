from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.accounts.models import User
from apps.accounts.services.user_directory_service import UserDirectoryService


class UserReplaceRoleView(LoginRequiredMixin, View):
    """تعویض نقش بین دو کاربر"""

    def post(self, request, user_id):
        old_user = get_object_or_404(User, id=user_id)
        new_user_id = request.POST.get("new_user_id")
        role = request.POST.get("role")
        group_id = request.POST.get("scientific_group")

        if not new_user_id or not role or not group_id:
            messages.error(request, "همه فیلدها الزامی است.")
            return redirect("accounts:admin-user-directory")

        new_user = get_object_or_404(User, id=new_user_id)

        result = UserDirectoryService.replace_role(old_user, new_user, role, group_id)

        if result["old_user_is_guest"]:
            messages.success(request, f"نقش منتقل شد. {old_user.get_full_name()} حالا مهمان است.")
        else:
            messages.success(request, f"نقش منتقل شد. {old_user.get_full_name()} نقش‌های دیگری هم دارد.")

        return redirect("accounts:admin-user-directory")
