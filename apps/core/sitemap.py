from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.shortcuts import resolve_url

from apps.assessments.models import Assessment


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["core:home", "core:assessments", "core:courses"]

    def location(self, item):
        return reverse(item)


class AssessmentSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Assessment.objects.filter(is_active=True)

    def location(self, obj):
        return reverse("core:assessment-detail", args=[obj.id])

    def lastmod(self, obj):
        return obj.updated_at
