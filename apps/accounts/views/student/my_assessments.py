from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class MyAssessmentsView(LoginRequiredMixin, TemplateView):
    """صفحه انتخاب نوع آزمون"""

    template_name = "dashboard/student/my_assessments.html"