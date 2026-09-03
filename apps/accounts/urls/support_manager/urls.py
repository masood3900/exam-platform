from django.urls import path

from apps.accounts.views.support_manager.dashboard import SupportManagerDashboardView
from apps.accounts.views.support_manager.contact import ContactSupportView
from apps.accounts.views.support_manager.tickets import SupportTicketListView, SupportTicketStatusChangeView

app_name = "support_manager"

urlpatterns = [
    path("dashboard/", SupportManagerDashboardView.as_view(), name="dashboard"),
    path("contact/", ContactSupportView.as_view(), name="contact"),
    path("tickets/", SupportTicketListView.as_view(), name="tickets"),
    path("tickets/<int:ticket_id>/status/", SupportTicketStatusChangeView.as_view(), name="ticket-status"),
]
