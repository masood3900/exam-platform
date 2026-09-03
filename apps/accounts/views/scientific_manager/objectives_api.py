from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.assessments.models import LearningObjective


class ObjectivesAPIView(LoginRequiredMixin, View):
    """اهداف یک موضوع"""

    def get(self, request, topic_id):
        objectives = LearningObjective.objects.filter(
            scientific_group_id=topic_id,
            is_active=True,
        )
        
        data = [
            {"id": str(obj.id), "code": obj.code, "name": obj.name}
            for obj in objectives
        ]
        
        return JsonResponse({"objectives": data})
