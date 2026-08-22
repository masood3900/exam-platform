from django.contrib.auth.forms import UserCreationForm

from apps.accounts.models import User


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

        super().__init__(
            *args,
            **kwargs,
        )

        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "form-control"
            )

        self.fields["username"].widget.attrs[
            "placeholder"
        ] = "نام کاربری"

        self.fields["email"].widget.attrs[
            "placeholder"
        ] = "example@gmail.com"

        self.fields["password1"].widget.attrs[
            "placeholder"
        ] = "رمز عبور"

        self.fields["password2"].widget.attrs[
            "placeholder"
        ] = "تکرار رمز عبور"

        self.fields["password1"].help_text = (
            "رمز عبور حداقل ۸ کاراکتر باشد و خیلی شبیه نام کاربری نباشد."
        )

        self.fields["password2"].help_text = (
            "رمز عبور را دوباره وارد کنید."
        )
