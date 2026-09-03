from django.urls import include, path
from apps.accounts.views.revenue_chart import RevenueChartView

app_name = "accounts"
urlpatterns = [
    path("revenue-chart/", RevenueChartView.as_view(), name="revenue-chart"),
    path(
        "",
        include("apps.accounts.urls.auth"),
    ),
    path(
        "admin/",
        include("apps.accounts.urls.admin"),
    ),
    path(
        "",
        include("apps.accounts.urls.student"),
    ),
    # path(
    #     "",
    #     include("apps.accounts.urls.instructor"),
    # ),
    path(
        "",
        include("apps.accounts.urls.profile"),
    ),
    path(
        "scientific-manager/",
        include("apps.accounts.urls.scientific_manager"),
    ),
    path(
        "question-designer/",
        include("apps.accounts.urls.question_designer"),
    ),
    path(
        "support-manager/",
        include("apps.accounts.urls.support_manager.urls"),
    ),
    path(
        "domain-manager/",
        include("apps.accounts.urls.domain_manager"),
    ),
    path(
        "financial-manager/",
        include("apps.accounts.urls.financial_manager"),
    ),
]