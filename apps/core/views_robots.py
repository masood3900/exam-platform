from django.http import HttpResponse
from django.views import View


class RobotsTxtView(View):
    def get(self, request):
        content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /accounts/
Disallow: /messaging/
"""
        return HttpResponse(content, content_type="text/plain")
