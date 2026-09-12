from django import forms
import jdatetime

from apps.accounts.models import UserProfile


class UserProfileForm(forms.ModelForm):

    first_name = forms.CharField(label="نام", required=False)
    last_name = forms.CharField(label="نام خانوادگی", required=False)
    email = forms.EmailField(label="ایمیل", required=False)

    birth_date_jalali = forms.CharField(
        label="تاریخ تولد",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "مثال: ۱۳۷۰/۰۵/۱۵",
            "readonly": "readonly",
            "id": "birthDateInput",
        }),
    )

    class Meta:
        model = UserProfile
        fields = (
            "first_name",
            "last_name",
            "email",
            "national_code",
            "birth_date",
            "phone",
            "gender",
            "avatar",
        )
        widgets = {
            "birth_date": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.instance.user
        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name
        self.fields["email"].initial = user.email

        if self.instance.birth_date:
            try:
                jalali = jdatetime.date.fromgregorian(date=self.instance.birth_date)
                self.fields["birth_date_jalali"].initial = (
                    f"{jalali.year}/{jalali.month:02d}/{jalali.day:02d}"
                )
            except Exception:
                pass

        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

        self.fields["gender"].widget.attrs["class"] = "form-select"

        # ترتیب دلخواه فیلدها
        self.order_fields([
            "first_name",
            "last_name",
            "email",
            "national_code",
            "birth_date_jalali",
            "phone",
            "gender",
            "avatar",
        ])

    def clean_birth_date_jalali(self):
        value = self.cleaned_data.get("birth_date_jalali", "").strip()

        if not value:
            return None

        for fa, en in zip("۰۱۲۳۴۵۶۷۸۹", "0123456789"):
            value = value.replace(fa, en)

        try:
            parts = value.split("/")
            if len(parts) != 3:
                raise ValueError("فرمت نامعتبر")

            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            jalali = jdatetime.date(year, month, day)
            return jalali.togregorian()
        except Exception:
            raise forms.ValidationError("تاریخ وارد شده معتبر نیست. مثال: ۱۳۷۰/۰۵/۱۵")

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.birth_date = self.cleaned_data.get("birth_date_jalali")

        if commit:
            profile.save()

            user = profile.user
            user.first_name = self.cleaned_data.get("first_name", "")
            user.last_name = self.cleaned_data.get("last_name", "")
            user.email = self.cleaned_data.get("email", "")
            user.save()

        return profile
