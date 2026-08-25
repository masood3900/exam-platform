from django.contrib import admin

from apps.assessments.models import AssessmentEnrollment


@admin.register(AssessmentEnrollment)
class AssessmentEnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "assessment",
        "status",
        "payment_status",
        "enrolled_at",
        "activated_at",
        "activated_by",
    )

    list_filter = (
        "status",
        "payment_status",
        "assessment__assessment_type",
        "assessment__learning_path",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "assessment__code",
        "assessment__title",
    )

    ordering = (
        "-enrolled_at",
    )

    list_select_related = (
        "user",
        "assessment",
        "assessment__learning_path",
        "activated_by",
    )

    autocomplete_fields = (
        "user",
        "assessment",
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
                    "assessment",
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