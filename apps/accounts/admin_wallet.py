from django.contrib import admin
from apps.accounts.models_wallet import Wallet, Transaction


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
