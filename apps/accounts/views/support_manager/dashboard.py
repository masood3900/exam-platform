from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.messaging.models import DirectMessage


class SupportManagerDashboardView(LoginRequiredMixin, TemplateView):
    """داشبورد مدیر پشتیبانی"""

    template_name = "dashboard/support_manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        from django.contrib.auth import get_user_model
        User = get_user_model()

        context["received_messages"] = DirectMessage.objects.filter(
            receiver=user,
        ).order_by("-created_at")[:10]

        context["unread_messages"] = DirectMessage.objects.filter(
            receiver=user,
            read_at__isnull=True,
        ).order_by("-created_at")

        context["read_messages"] = DirectMessage.objects.filter(
            receiver=user,
            read_at__isnull=False,
        ).order_by("-created_at")[:10]

        context["unread_count"] = DirectMessage.objects.filter(
            receiver=user,
            read_at__isnull=True,
        ).count()

        context["total_messages"] = DirectMessage.objects.filter(
            receiver=user,
        ).count()

        context["active_conversations"] = DirectMessage.objects.filter(
            receiver=user,
            read_at__isnull=True,
        ).values("sender").distinct().count()

        # کاربران اخیر
        context["recent_users"] = User.objects.filter(
            is_active=True,
        ).order_by("-date_joined")[:5]

        # تیکت‌ها
        from apps.messaging.models import Ticket
        context["recent_tickets"] = Ticket.objects.all().order_by("-created_at")[:5]

        return context
