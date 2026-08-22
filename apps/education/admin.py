from django.contrib import admin

from .models import InstructorAssignment


@admin.register(InstructorAssignment)
class InstructorAssignmentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "instructor",
        "learning_path",
        "course",
        "is_active",
        "started_at",
        "ended_at",
    )

    list_filter = (
        "is_active",
        "learning_path",
        "course",
        "instructor",
    )

    search_fields = (
        "student__username",
        "student__first_name",
        "student__last_name",
        "instructor__username",
        "instructor__first_name",
        "instructor__last_name",
        "learning_path__name",
        "course__name",
    )

    ordering = (
        "-started_at",
    )

    list_select_related = (
        "student",
        "instructor",
        "learning_path",
        "course",
    )

    autocomplete_fields = (
        "student",
        "instructor",
        "learning_path",
        "course",
    )

    readonly_fields = (
        "started_at",
        "created_at",
    )

    fieldsets = (
        (
            "افراد",
            {
                "fields": (
                    "student",
                    "instructor",
                )
            },
        ),
        (
            "محدوده آموزشی",
            {
                "fields": (
                    "learning_path",
                    "course",
                ),
                "description": (
                    "تخصیص می‌تواند برای یک مسیر آموزشی یا یک دوره "
                    "انجام شود. حداقل یکی از این دو باید مشخص باشد."
                ),
            },
        ),
        (
            "وضعیت",
            {
                "fields": (
                    "is_active",
                    "started_at",
                    "ended_at",
                )
            },
        ),
        (
            "اطلاعات سیستمی",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )

    list_per_page = 25