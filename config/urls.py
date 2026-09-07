from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from apps.core.views_robots import RobotsTxtView
from apps.assessments.models import Assessment


def custom_sitemap(request):
    base_url = "http://sanjehyar.ir"
    
    urls = [
        f"{base_url}/",
        f"{base_url}/assessments/",
        f"{base_url}/courses/",
    ]
    
    for assessment in Assessment.objects.filter(is_active=True):
        urls.append(f"{base_url}/assessments/{assessment.id}/")
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for url in urls:
        xml.append(f'<url><loc>{url}</loc></url>')
    
    xml.append('</urlset>')
    
    return HttpResponse("\n".join(xml), content_type="application/xml")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.core.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("assessments/", include("apps.assessments.urls")),
    path("messaging/", include("apps.messaging.urls")),
    path("sitemap.xml", custom_sitemap, name="sitemap"),
    path("robots.txt", RobotsTxtView.as_view(), name="robots"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
