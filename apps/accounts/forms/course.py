from django import forms

from apps.assessments.models import Course


class CourseForm(forms.ModelForm):

    class Meta:

        model = Course

        fields = (
            "learning_path",
            "parent",
            "code",
            "name",
            "description",
            "price",
            "discount_percent",
            "prerequisites",
            "order",
            "estimated_minutes",
            "is_active",
        )

        labels = {
            "learning_path": "مسیر آموزشی",
            "parent": "دوره والد",
            "code": "کد دوره",
            "name": "نام دوره",
            "description": "توضیحات دوره",
            "price": "قیمت",
            "discount_percent": "درصد تخفیف",
            "prerequisites": "پیش‌نیازها",
            "order": "ترتیب نمایش",
            "estimated_minutes": "زمان تقریبی یادگیری (دقیقه)",
            "is_active": "فعال",
        }

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),
            "prerequisites": forms.SelectMultiple(),
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

            field.widget.attrs["class"] = (
                "form-control"
            )

        self.fields["learning_path"].widget.attrs[
            "class"
        ] = "form-select"

        self.fields["parent"].widget.attrs[
            "class"
        ] = "form-select"

        self.fields["prerequisites"].widget.attrs[
            "class"
        ] = "form-select"
