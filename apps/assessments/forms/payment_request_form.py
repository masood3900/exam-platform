from django import forms

from apps.assessments.models import PaymentRequest


class PaymentRequestForm(forms.ModelForm):
    """فرم درخواست پرداخت"""

    class Meta:
        model = PaymentRequest
        fields = [
            "tracking_code",
            "receipt_image",
        ]
        widgets = {
            "tracking_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "کد رهگیری پرداخت را وارد کنید...",
            }),
            "receipt_image": forms.FileInput(attrs={
                "class": "form-control",
            }),
        }