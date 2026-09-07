from django.contrib import admin
from apps.messaging.models import DirectMessage, Ticket


@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ["id", "sender", "receiver", "text", "read_at", "created_at"]
    list_filter = ["read_at", "created_at"]
    search_fields = ["sender__username", "receiver__username", "text"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["title", "user__username"]
