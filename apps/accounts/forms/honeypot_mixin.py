from django import forms


class HoneypotMixin:
    """جلوگیری از ربات با Honeypot"""

    honeypot_field = "website_url"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.honeypot_field] = forms.CharField(
            required=False,
            widget=forms.TextInput(
                attrs={
                    "style": "display:none;",
                    "tabindex": "-1",
                    "autocomplete": "off",
                }
            ),
            label="",
        )

    def clean(self):
        cleaned_data = super().clean()
        honeypot_value = cleaned_data.get(self.honeypot_field)

        if honeypot_value:
            raise forms.ValidationError("خطای امنیتی! لطفاً دوباره تلاش کنید.")

        return cleaned_data
