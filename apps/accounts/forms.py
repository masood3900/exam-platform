from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, UserProfile


class UserRegisterForm(UserCreationForm):

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

class UserProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        label="نام",
        required=False,
    )

    last_name = forms.CharField(
        label="نام خانوادگی",
        required=False,
    )

    email = forms.EmailField(
        label="ایمیل",
        required=False,
    )

    class Meta:

        model = UserProfile

        fields = (
            "first_name",
            "last_name",
            "email",
            "national_code",
            "phone",
            "birth_date",
            "gender",
            "avatar",
        )

        widgets = {
            "birth_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            )
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        user = self.instance.user

        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name
        self.fields["email"].initial = user.email

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["gender"].widget.attrs["class"] = "form-select"

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()

        return profile