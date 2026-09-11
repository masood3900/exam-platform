from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views import View
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


class PasswordResetRequestView(View):
    """درخواست بازیابی رمز"""

    template_name = "accounts/password_reset_request.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")

        if not email:
            messages.error(request, "ایمیل را وارد کنید.")
            return render(request, self.template_name)

        user = User.objects.filter(email=email).first()

        if user:
            # ساخت توکن
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # لینک بازیابی
            reset_url = f"http://sanjehyar.ir/accounts/password-reset-confirm/{uid}/{token}/"

            # ارسال ایمیل
            send_mail(
                "بازیابی رمز عبور سنجه‌یار",
                f"برای تغییر رمز عبور روی لینک زیر کلیک کنید:\n\n{reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

        messages.success(
            request,
            "اگر ایمیل وارد شده در سیستم باشد، لینک بازیابی ارسال شد.",
        )
        return redirect("accounts:login")


class PasswordResetConfirmView(View):
    """تایید و تغییر رمز"""

    template_name = "accounts/password_reset_confirm.html"

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            return render(request, self.template_name, {"valid": True})

        messages.error(request, "لینک نامعتبر است.")
        return redirect("accounts:login")

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if not password1 or not password2:
                messages.error(request, "هر دو فیلد الزامی است.")
                return render(request, self.template_name, {"valid": True})

            if password1 != password2:
                messages.error(request, "رمز عبور مطابقت ندارد.")
                return render(request, self.template_name, {"valid": True})

            if len(password1) < 8:
                messages.error(request, "رمز عبور حداقل ۸ کاراکتر باشد.")
                return render(request, self.template_name, {"valid": True})

            from django.contrib.auth.hashers import make_password
            user.password = make_password(password1)
            user.save()

            messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
            return redirect("accounts:login")

        messages.error(request, "لینک نامعتبر است.")
        return redirect("accounts:login")
