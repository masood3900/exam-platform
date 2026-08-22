from django import forms

from apps.accounts.models import UserProfile


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

    def __init__(
        self,
        *args,
        **kwargs,
    ):

        super().__init__(
            *args,
            **kwargs
        )

        user = self.instance.user

        self.fields["first_name"].initial = (
            user.first_name
        )

        self.fields["last_name"].initial = (
            user.last_name
        )

        self.fields["email"].initial = (
            user.email
        )

        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "form-control"
            )

        self.fields["gender"].widget.attrs[
            "class"
        ] = "form-select"

    def save(self, commit=True):

        profile = super().save(
            commit=False
        )

        if commit:
            profile.save()

        return profile
