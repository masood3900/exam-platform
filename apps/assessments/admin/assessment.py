from django.contrib import admin
from apps.assessments.models import (
    Assessment,
    AssessmentRule,
)

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "title",
        "assessment_type",
        "duration_minutes",
        "passing_score",
        "is_active",
    )

    list_filter = (
        "assessment_type",
        "is_active",
    )

    search_fields = (
        "code",
        "title",
    )
    ordering = ("assessment_type", "title")
    list_per_page = 25
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(AssessmentRule)
class AssessmentRuleAdmin(admin.ModelAdmin):

    list_display = (
        "assessment",
        "category",
        "learning_objective",
        "difficulty",
        "question_count",
    )

    list_filter = (
        "assessment",
        "category",
        "difficulty",
    )

    search_fields = (
        "assessment__code",
        "assessment__title",
        "category__code",
        "category__name",
        "learning_objective__code",
        "learning_objective__name",
    )

    ordering = (
        "assessment",
        "category",
        "learning_objective",
    )

    list_per_page = 25

    list_select_related = (
        "assessment",
        "category",
        "learning_objective",
    )

    autocomplete_fields = (
        "assessment",
        "category",
        "learning_objective",
    )