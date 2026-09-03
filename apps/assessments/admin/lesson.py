from django.contrib import admin

from apps.assessments.models import (
    Lesson,
    Exercise,
    ExerciseAttempt,
    UserScore,
)


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1
    fields = (
        "title",
        "exercise_type",
        "language",
        "order",
        "points",
        "is_active",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "category",
        "order",
        "is_free",
        "is_active",
    )
    list_filter = ("is_free", "is_active", "course")
    search_fields = ("title", "content", "course__name")
    ordering = ("course", "order")
    list_select_related = ("course", "category")
    inlines = [ExerciseInline]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "lesson",
        "exercise_type",
        "language",
        "order",
        "points",
        "is_active",
    )
    list_filter = ("exercise_type", "language", "is_active", "lesson")
    search_fields = ("title", "body", "lesson__title")
    autocomplete_fields = ("lesson",)


@admin.register(ExerciseAttempt)
class ExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "exercise",
        "is_correct",
        "score_earned",
        "created_at",
    )
    list_filter = ("is_correct", "created_at")
    search_fields = ("user__username", "exercise__title")
    readonly_fields = ("created_at",)


@admin.register(UserScore)
class UserScoreAdmin(admin.ModelAdmin):
    list_display = ("user", "total_score", "updated_at")
    search_fields = ("user__username",)
    ordering = ("-total_score",)