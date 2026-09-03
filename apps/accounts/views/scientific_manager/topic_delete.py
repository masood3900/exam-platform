from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.assessments.models import ScientificGroup


class TopicDeleteView(LoginRequiredMixin, View):
    """حذف موضوع"""

    def post(self, request, topic_id):
        topic = get_object_or_404(ScientificGroup, id=topic_id)
        
        topic_name = topic.name
        topic.delete()
        
        messages.success(request, f"موضوع «{topic_name}» حذف شد.")
        return redirect("accounts:scientific_manager:dashboard")