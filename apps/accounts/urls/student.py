from django.urls import path

from apps.accounts.views.student.dashboard import (
    DashboardView,
)
from apps.accounts.views.student.assessment_enroll import (
    AssessmentEnrollView,
)
from apps.accounts.views.student.payment_request import (
    PaymentRequestView,
)
from apps.accounts.views.student.payment_status import (
    PaymentStatusView,
)
from apps.accounts.views.student.my_assessments import (
    MyAssessmentsView,
)
from apps.accounts.views.student.my_free_assessments import (
    MyFreeAssessmentsView,
)
from apps.accounts.views.student.my_paid_assessments import (
    MyPaidAssessmentsView,
)
from apps.accounts.views.student.assessment_remove import AssessmentRemoveView
from apps.accounts.views.student.contact_manager import ContactManagerView

urlpatterns = [
    path(
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard",
    ),
    path(
        "assessment/<uuid:assessment_id>/enroll/",
        AssessmentEnrollView.as_view(),
        name="assessment-enroll",
    ),
    path(
        "payment/assessment/<uuid:assessment_id>/",
        PaymentRequestView.as_view(),
        name="payment-request-assessment",
    ),
    path(
        "payment/status/",
        PaymentStatusView.as_view(),
        name="payment-status",
    ),
    path(
        "my-assessments/",
        MyAssessmentsView.as_view(),
        name="my-assessments",
    ),
    path(
        "my-assessments/free/",
        MyFreeAssessmentsView.as_view(),
        name="my-free-assessments",
    ),
    path(
        "my-assessments/paid/",
        MyPaidAssessmentsView.as_view(),
        name="my-paid-assessments",
    ),
    path("assessment/enrollment/<int:enrollment_id>/remove/", AssessmentRemoveView.as_view(), name="assessment-remove"),
    path("assessment/<uuid:assessment_id>/contact-manager/", ContactManagerView.as_view(), name="contact-manager"),
]
