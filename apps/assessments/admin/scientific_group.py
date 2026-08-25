from django.contrib import admin

from apps.assessments.models import (
    ScientificGroup,
    ScientificGroupMembership,
)


@admin.register(ScientificGroup)
class ScientificGroupAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "code",
        "name",
        "description",
    )

    ordering = (
        "name",
    )


@admin.register(ScientificGroupMembership)
class ScientificGroupMembershipAdmin(admin.ModelAdmin):

    list_display = (
        "scientific_group",
        "user",
        "role",
        "is_active",
        "joined_at",
    )

    list_filter = (
        "role",
        "is_active",
        "scientific_group",
    )

    search_fields = (
        "scientific_group__name",
        "scientific_group__code",
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    ordering = (
        "scientific_group",
        "user",
    )

    autocomplete_fields = (
        "scientific_group",
        "user",
    )

    readonly_fields = (
        "joined_at",
    )