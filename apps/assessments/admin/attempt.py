from django.contrib import admin
from apps.assessments.models import (
   Attempt,
 
)

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):

    list_display = (
        "assessment",
        "student",
        "status",
        "percentage",
        "passed",
        "started_at",
    )
    readonly_fields = (
        "started_at",
        "submitted_at",
        "total_questions",
        "correct_answers",
        "score",
        "percentage",
        "passed",
    )

    list_filter = (
        "assessment",
        "status",
        "passed",
    )

    search_fields = (
        "student__username",
        "student__first_name",
        "student__last_name",
        "assessment__code",
        "assessment__title",
    )

    ordering = (
        "-started_at",
    )
    list_per_page = 25

    list_select_related = (
        "assessment",
        "student",
    )
    autocomplete_fields = (
        "assessment",
        "student",
    )