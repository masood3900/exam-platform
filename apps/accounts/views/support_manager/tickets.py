from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages

from apps.messaging.models import Ticket


class SupportTicketListView(LoginRequiredMixin, ListView):
    """لیست تیکت‌ها برای پشتیبان"""

    model = Ticket
    template_name = "dashboard/support_manager/tickets.html"
    context_object_name = "tickets"
    paginate_by = 20

    def get_queryset(self):
        return Ticket.objects.all().select_related("user").order_by("-created_at")


class SupportTicketStatusChangeView(LoginRequiredMixin, View):
    """تغییر وضعیت تیکت"""

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        new_status = request.POST.get("status")

        if new_status in ["open", "in_progress", "closed"]:
            ticket.status = new_status
            ticket.save()
            messages.success(request, f"وضعیت تیکت #{ticket.id} تغییر کرد.")

        return redirect("accounts:support_manager:tickets")
