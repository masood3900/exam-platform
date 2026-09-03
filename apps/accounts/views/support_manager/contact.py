from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from apps.assessments.models import ScientificGroupMembership


class ContactSupportView(LoginRequiredMixin, TemplateView):
    """ارتباط با مدیر پشتیبانی"""

    template_name = "dashboard/support_manager/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # پیدا کردن مدیر پشتیبانی
        support_membership = ScientificGroupMembership.objects.filter(
            role="support_manager",
            is_active=True,
        ).select_related("user").first()

        if support_membership:
            context["support_manager"] = support_membership.user
        else:
            context["support_manager"] = None

        return context
