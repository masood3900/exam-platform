from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.forms.honeypot_mixin import HoneypotMixin
from apps.accounts.models import User


class UserRegisterForm(HoneypotMixin, UserCreationForm):

    referral_code_input = forms.CharField(
        label="کد معرف (اختیاری)",
        required=False,
        max_length=10,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "مثلاً SJ12345",
            }
        ),
    )

    class Meta(UserCreationForm.Meta):

        model = User

        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

        labels = {
            "username": "نام کاربری",
            "email": "ایمیل",
            "password1": "رمز عبور",
            "password2": "تکرار رمز عبور",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["username"].widget.attrs["placeholder"] = "نام کاربری"
        self.fields["email"].widget.attrs["placeholder"] = "example@gmail.com"
        self.fields["password1"].widget.attrs["placeholder"] = "رمز عبور"
        self.fields["password2"].widget.attrs["placeholder"] = "تکرار رمز عبور"

        self.fields["password1"].help_text = (
            "رمز عبور حداقل ۸ کاراکتر باشد و خیلی شبیه نام کاربری نباشد."
        )
        self.fields["password2"].help_text = (
            "رمز عبور را دوباره وارد کنید."
        )

    def clean_referral_code_input(self):
        code = self.cleaned_data.get("referral_code_input", "").strip().upper()

        if code:
            try:
                referrer = User.objects.get(referral_code__iexact=code)
            except User.DoesNotExist:
                raise forms.ValidationError("کد معرف نامعتبر است.")
            return referrer

        return None

    def save(self, commit=True):
        user = super().save(commit=False)
        referrer = self.cleaned_data.get("referral_code_input")

        if referrer:
            user.referred_by = referrer

        if commit:
            user.save()

        return user
