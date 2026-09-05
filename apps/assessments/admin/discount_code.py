from django.contrib import admin

from apps.assessments.models import DiscountCode, DiscountCodeUsage


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "discount_percent",
        "assessment",
        "valid_from",
        "valid_until",
        "used_count",
        "max_uses",
        "is_active",
        "created_at",
    ]
    list_filter = [
        "is_active",
        "assessment",
        "valid_until",
    ]
    search_fields = [
        "code",
        "assessment__title",
    ]
    readonly_fields = [
        "used_count",
        "created_at",
        "updated_at",
    ]


@admin.register(DiscountCodeUsage)
class DiscountCodeUsageAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "user",
        "assessment",
        "discount_percent",
        "original_price",
        "discounted_price",
        "created_at",
    ]
    list_filter = [
        "code",
        "created_at",
    ]
    search_fields = [
        "code__code",
        "user__username",
        "assessment__title",
    ]
    readonly_fields = [
        "created_at",
    ]
