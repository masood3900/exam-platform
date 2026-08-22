from django.contrib import admin

from apps.assessments.models import (
    LearningPath,
    UserLearningPath,
)


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "color",
        "order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "slug",
    )

    ordering = (
        "order",
        "name",
    )


@admin.register(UserLearningPath)
class UserLearningPathAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "learning_path",
        "started_at",
        "is_active",
        "completed_at",
    )

    list_filter = (
        "learning_path",
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "learning_path__name",
    )

    ordering = (
        "-started_at",
    )

    list_select_related = (
        "user",
        "learning_path",
    )

    autocomplete_fields = (
        "user",
        "learning_path",
    )

    list_per_page = 25