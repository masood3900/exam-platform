from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.messaging.models import Ticket


class TicketListView(LoginRequiredMixin, ListView):
    """لیست تیکت‌های کاربر"""

    model = Ticket
    template_name = "messaging/ticket_list.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user).order_by("-created_at")
