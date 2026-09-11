from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.accounts.models_wallet import Wallet, Transaction


class WalletView(LoginRequiredMixin, TemplateView):
    """صفحه کیف پول کاربر"""

    template_name = "accounts/wallet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)

        context["wallet"] = wallet
        context["transactions"] = wallet.transactions.all()[:50]

        return context
