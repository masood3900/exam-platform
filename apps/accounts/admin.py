from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


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