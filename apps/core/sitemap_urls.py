from django.urls import path
from django.contrib.sitemaps.views import sitemap

from apps.core.sitemap import StaticViewSitemap, AssessmentSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "assessments": AssessmentSitemap,
}

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", __import__("django").views.static.serve, {"document_root": "templates/", "path": "robots.txt"}),
]
