from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from apps.messaging.models import Ticket


class TicketCreateView(LoginRequiredMixin, View):
    """ساخت تیکت جدید"""

    template_name = "messaging/ticket_create.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority", "normal")

        if not title or not description:
            messages.error(request, "عنوان و توضیحات الزامی است.")
            return redirect("messaging:ticket-create")

        Ticket.objects.create(
            user=request.user,
            title=title,
            description=description,
            priority=priority,
        )

        messages.success(request, "تیکت شما ثبت شد.")
        return redirect("messaging:ticket-list")
