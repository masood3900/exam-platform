from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.accounts.models import User


class ReferralsView(LoginRequiredMixin, TemplateView):
    """لیست افراد معرفی‌شده"""

    template_name = "accounts/referrals.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        referred_users = User.objects.filter(
            referred_by=self.request.user
        ).order_by("-date_joined")

        context["referred_users"] = referred_users
        context["referred_users_count"] = referred_users.count()

        return context
