from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.assessments.models import LearningObjective


class LearningObjectivesAPIView(LoginRequiredMixin, View):
    """دریافت اهداف آموزشی بر اساس گروه علمی"""

    def get(self, request, course_id):
        
        objectives = LearningObjective.objects.filter(
            category__course_id=course_id,
            is_active=True,
        ).select_related(
            "category",
            "category__course",
        )
        
        data = [
            {
                "id": str(obj.id),
                "name": obj.name,
                "code": obj.code,
                "category": obj.category.name,
                "course": obj.category.course.name,
            }
            for obj in objectives
        ]
        
        return JsonResponse({"objectives": data})