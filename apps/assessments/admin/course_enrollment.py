from django.contrib import admin

from apps.assessments.models import CourseEnrollment


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "course",
        "status",
        "payment_status",
        "enrolled_at",
        "activated_at",
        "activated_by",
    )

    list_filter = (
        "status",
        "payment_status",
        "course__learning_path",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "course__code",
        "course__name",
    )

    ordering = (
        "-enrolled_at",
    )

    list_select_related = (
        "user",
        "course",
        "course__learning_path",
        "activated_by",
    )

    autocomplete_fields = (
        "user",
        "course",
        "activated_by",
    )

    readonly_fields = (
        "enrolled_at",
        "activated_at",
    )

    fieldsets = (
        (
            "ثبت‌نام",
            {
                "fields": (
                    "user",
                    "course",
                    "enrolled_at",
                )
            },
        ),
        (
            "وضعیت دسترسی و پرداخت",
            {
                "fields": (
                    "status",
                    "payment_status",
                ),
                "description": (
                    "در نسخه فعلی، پرداخت به صورت دستی انجام می‌شود. "
                    "پس از دریافت وجه، مدیر می‌تواند وضعیت پرداخت و "
                    "دسترسی دانش‌آموز را فعال کند."
                ),
            },
        ),
        (
            "فعال‌سازی",
            {
                "fields": (
                    "activated_at",
                    "activated_by",
                )
            },
        ),
    )

    list_per_page = 25