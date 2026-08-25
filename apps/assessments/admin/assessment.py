from django.contrib import admin
from apps.assessments.models import (
    Assessment,
    AssessmentRule,
    LearningObjective,
)
from django import forms


class AssessmentRuleInline(admin.TabularInline):
    model = AssessmentRule
    
    extra = 1

    fields = (
        "category",
        "learning_objective",
        "difficulty",
        "question_count",
    )

    autocomplete_fields = (
        "category",
        "learning_objective",
    )

    min_num = 1


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


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    inlines = [
    AssessmentRuleInline,
    ]

    list_display = (
        "code",
        "title",
        "assessment_type",
        "learning_path",
        "course",
        "price",
        "discount_percent",
        "final_price_display",
        "demo_attempts",
        "max_attempts",
        "is_active",
    )

    list_filter = (
        "assessment_type",
        "learning_path",
        "is_active",
    )

    search_fields = (
        "code",
        "title",
        "learning_path__name",
        "course__code",
        "course__name",
    )
    autocomplete_fields = (
        "learning_path",
        "course",
        "objectives",
        "created_by",
    )
    list_select_related = (
        "learning_path",
        "course",
        "created_by",
    )
    ordering = ("assessment_type", "title")
    list_per_page = 25

    @admin.display(
        description="قیمت نهایی",
        ordering="price",
    )
    def final_price_display(self, obj):
        return obj.final_price


    readonly_fields = (
        "final_price_display",
        "created_at",
        "updated_at",
    )

