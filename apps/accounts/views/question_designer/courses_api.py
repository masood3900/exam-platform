from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.assessments.models import Course


class CoursesAPIView(LoginRequiredMixin, View):
    """دریافت دوره‌ها بر اساس گروه علمی"""

    def get(self, request, group_id):
        
        courses = Course.objects.filter(
            scientific_group_id=group_id,
            is_active=True,
            parent__isnull=False,
        )
        
        data = [
            {
                "id": str(course.id),
                "name": course.name,
                "code": course.code,
            }
            for course in courses
        ]
        
        return JsonResponse({"courses": data})