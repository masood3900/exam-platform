from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from apps.accounts.mixins import AdminRequiredMixin

User = get_user_model()


class UserManagementView(AdminRequiredMixin, View):
    """مدیریت کامل کاربران"""

    template_name = "dashboard/admin/user_management.html"

    def get(self, request):
        users = User.objects.all().order_by("-date_joined")
        return render(request, self.template_name, {"users": users})

    def post(self, request):
        action = request.POST.get("action")

        if action == "create":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            first_name = request.POST.get("first_name", "")
            last_name = request.POST.get("last_name", "")
            is_staff = request.POST.get("is_staff") == "on"
            is_superuser = request.POST.get("is_superuser") == "on"
            is_active = request.POST.get("is_active") == "on"

            if not username or not password:
                messages.error(request, "نام کاربری و رمز عبور الزامی است.")
                return redirect("accounts:user-management")

            if User.objects.filter(username=username).exists():
                messages.error(request, "این نام کاربری قبلاً استفاده شده.")
                return redirect("accounts:user-management")

            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_superuser=is_superuser,
                is_active=is_active,
            )
            messages.success(request, f"کاربر «{username}» ساخته شد.")
            return redirect("accounts:user-management")

        elif action == "update":
            user_id = request.POST.get("user_id")
            user = get_object_or_404(User, id=user_id)

            user.username = request.POST.get("username")
            user.email = request.POST.get("email")
            user.first_name = request.POST.get("first_name", "")
            user.last_name = request.POST.get("last_name", "")
            user.is_staff = request.POST.get("is_staff") == "on"
            user.is_superuser = request.POST.get("is_superuser") == "on"
            user.is_active = request.POST.get("is_active") == "on"

            new_password = request.POST.get("password")
            if new_password:
                user.password = make_password(new_password)

            user.save()
            messages.success(request, f"کاربر «{user.username}» به‌روزرسانی شد.")
            return redirect("accounts:user-management")

        elif action == "delete":
            user_id = request.POST.get("user_id")
            user = get_object_or_404(User, id=user_id)
            username = user.username
            user.delete()
            messages.success(request, f"کاربر «{username}» حذف شد.")
            return redirect("accounts:user-management")

        return redirect("accounts:user-management")
