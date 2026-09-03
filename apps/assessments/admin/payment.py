from django.contrib import admin

from apps.assessments.models import PaymentAccount, PaymentRequest


@admin.register(PaymentAccount)
class PaymentAccountAdmin(admin.ModelAdmin):
    list_display = ("title", "account_type", "account_number", "owner_name", "is_active")
    list_filter = ("account_type", "is_active")
    search_fields = ("title", "account_number", "owner_name")


@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "status", "created_at", "tracking_code")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "tracking_code")
    readonly_fields = ("created_at", "reviewed_at")