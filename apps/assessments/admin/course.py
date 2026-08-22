from django.contrib import admin

from apps.assessments.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "learning_path",
        "parent",
        "price",
        "discount_percent",
        "final_price_display",
        "is_free_display",
        "order",
        "is_active",
    )

    list_filter = (
        "learning_path",
        "parent",
        "is_active",
        "discount_percent",
    )

    search_fields = (
        "code",
        "name",
        "parent__name",
    )

    ordering = (
        "learning_path",
        "order",
        "name",
    )

    list_select_related = (
        "learning_path",
        "parent",
    )

    autocomplete_fields = (
        "learning_path",
        "parent",
        "prerequisites",
    )

    fieldsets = (
        (
            "اطلاعات دوره",
            {
                "fields": (
                    "learning_path",
                    "parent",
                    "code",
                    "name",
                    "description",
                )
            },
        ),
        (
            "قیمت‌گذاری",
            {
                "fields": (
                    "price",
                    "discount_percent",
                ),
                "description": (
                    "قیمت پایه و درصد تخفیف توسط مدیر تعیین می‌شود. "
                    "قیمت صفر به معنی دوره رایگان است."
                ),
            },
        ),
        (
            "تنظیمات نمایش و دسترسی",
            {
                "fields": (
                    "order",
                    "estimated_minutes",
                    "is_active",
                )
            },
        ),
        (
            "پیش‌نیازها",
            {
                "fields": (
                    "prerequisites",
                )
            },
        ),
    )

    list_per_page = 25

    @admin.display(
        description="قیمت نهایی",
    )
    def final_price_display(self, obj):
        return f"{obj.final_price:,} تومان"

    @admin.display(
        description="وضعیت قیمت",
    )
    def is_free_display(self, obj):

        if obj.is_free:
            return "رایگان"

        if obj.has_discount:
            return f"{obj.discount_percent}% تخفیف"

        return "عادی"