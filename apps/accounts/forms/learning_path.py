from django import forms

from apps.assessments.models import LearningPath


class LearningPathForm(forms.ModelForm):

    class Meta:

        model = LearningPath

        fields = (
            "name",
            "slug",
            "description",
            "icon",
            "color",
            "prerequisites",
            "order",
            "is_active",
        )

        labels = {
            "name": "نام مسیر آموزشی",
            "slug": "شناسه مسیر",
            "description": "توضیحات",
            "icon": "آیکون",
            "color": "رنگ",
            "prerequisites": "پیش‌نیازها",
            "order": "ترتیب نمایش",
            "is_active": "فعال",
        }

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
            "prerequisites": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                }
            ),
            "is_active": forms.CheckboxInput(),
        }

    def __init__(
        self,
        *args,
        **kwargs,
    ):

        super().__init__(
            *args,
            **kwargs,
        )

        for name, field in self.fields.items():

            if name == "is_active":
                continue

            if name == "prerequisites":
                field.widget.attrs[
                    "class"
                ] = "form-select"

            else:
                field.widget.attrs[
                    "class"
                ] = "form-control"
