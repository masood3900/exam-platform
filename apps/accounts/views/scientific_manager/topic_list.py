from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.accounts.services.scientific_group_service import ScientificGroupService
from apps.accounts.models import User


class TopicListView(LoginRequiredMixin, TemplateView):
    """لیست موضوع‌های مدیر علمی"""

    template_name = "dashboard/scientific_manager/topic_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        fields = ScientificGroupService.get_manager_fields(user)
        topics = []
        for field in fields:
            topics.extend(ScientificGroupService.get_topics_of_field(field.id))
        
        context["topics"] = topics
        context["all_users"] = User.objects.filter(is_active=True)
        return context