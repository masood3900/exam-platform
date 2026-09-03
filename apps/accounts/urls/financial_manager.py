from django.urls import path

from apps.accounts.views.financial_manager.dashboard import FinancialManagerDashboardView
from apps.accounts.views.financial_manager.payment_review import FinancialPaymentReviewView
app_name = "financial_manager"

urlpatterns = [
    path("dashboard/", FinancialManagerDashboardView.as_view(), name="dashboard"),
    path(
        "payments/<uuid:payment_id>/review/",
        FinancialPaymentReviewView.as_view(),
        name="payment-review",
    ),
]