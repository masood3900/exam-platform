from django import forms


class DiscountCodeForm(forms.Form):
    """فرم ورود کد تخفیف"""

    code = forms.CharField(
        max_length=50,
        label="کد تخفیف",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "کد تخفیف را وارد کنید...",
            }
        ),
    )
