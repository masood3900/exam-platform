from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .models_wallet import Wallet, Transaction


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "gender",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "national_code",
        "phone",
    )

    ordering = (
        "username",
    )

    fieldsets = (
        ("اطلاعات ورود", {
            "fields": (
                "username",
                "password",
            )
        }),
        ("اطلاعات شخصی", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "national_code",
                "phone",
                "birth_date",
                "gender",
            )
        }),
        ("اطلاعات مالی و معرف", {
            "fields": (
                "bank_account_number",
                "bank_name",
                "referral_code",
                "referred_by",
            )
        }),
        ("دسترسی‌ها", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("تاریخ‌ها", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )

    add_fieldsets = (
        ("ایجاد کاربر", {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "first_name",
                "last_name",
                "national_code",
                "phone",
                "birth_date",
                "gender",
                "password1",
                "password2",
                "is_staff",
                "is_superuser",
                "is_active",
            ),
        }),
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["user", "balance", "is_active", "updated_at"]
    list_filter = ["is_active"]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    readonly_fields = ["balance", "created_at", "updated_at"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["wallet", "transaction_type", "amount", "balance_after", "created_at"]
    list_filter = ["transaction_type", "created_at"]
    search_fields = ["wallet__user__username", "description"]
    readonly_fields = ["created_at"]
