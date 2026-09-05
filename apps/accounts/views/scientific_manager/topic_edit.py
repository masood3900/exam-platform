from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.accounts.services.scientific_group_service import ScientificGroupService
from apps.assessments.models import ScientificGroup, LearningObjective


class TopicEditView(LoginRequiredMixin, View):
    """ویرایش موضوع و اهداف آموزشی"""

    template_name = "dashboard/scientific_manager/topic_edit.html"

    def get(self, request, topic_id):
        topic = get_object_or_404(ScientificGroup, id=topic_id)
        objectives = LearningObjective.objects.filter(
            scientific_group=topic,
        ).order_by("order", "code")

        return render(request, self.template_name, {
            "topic": topic,
            "objectives": objectives,
        })

    def post(self, request, topic_id):
        topic = get_object_or_404(ScientificGroup, id=topic_id)

        # به‌روزرسانی اطلاعات موضوع
        name = request.POST.get("name", "").strip()
        code = request.POST.get("code", "").strip()
        description = request.POST.get("description", "").strip()

        if name:
            topic.name = name
        if code:
            topic.code = code
        topic.description = description
        topic.save()

        messages.success(request, f"موضوع «{topic.name}» به‌روزرسانی شد.")
        return redirect("accounts:scientific_manager:topic-management")


class ObjectiveCreateView(LoginRequiredMixin, View):
    """افزودن هدف آموزشی به موضوع"""

    def post(self, request, topic_id):
        topic = get_object_or_404(ScientificGroup, id=topic_id)

        name = request.POST.get("name", "").strip()
        code = request.POST.get("code", "").strip()
        description = request.POST.get("description", "").strip()

        if not name or not code:
            messages.error(request, "نام و کد هدف الزامی است.")
            return redirect("accounts:scientific_manager:topic-edit", topic_id=topic.id)

        try:
            LearningObjective.objects.create(
                name=name,
                code=code,
                description=description,
                scientific_group=topic,
            )
            messages.success(request, f"هدف «{name}» اضافه شد.")
        except Exception as e:
            messages.error(request, f"خطا در ساخت هدف: {e}")

        return redirect("accounts:scientific_manager:topic-edit", topic_id=topic.id)


class ObjectiveDeleteView(LoginRequiredMixin, View):
    """حذف هدف آموزشی"""

    def post(self, request, objective_id):
        objective = get_object_or_404(LearningObjective, id=objective_id)
        topic_id = objective.scientific_group.id

        # بررسی وابستگی
        if objective.questions.exists() or objective.assessments.exists():
            messages.warning(
                request,
                f"هدف «{objective.name}» قابل حذف نیست، زیرا "
                f"سوال یا آزمونی به آن متصل است.",
            )
        else:
            objective_name = objective.name
            objective.delete()
            messages.success(request, f"هدف «{objective_name}» حذف شد.")

        return redirect("accounts:scientific_manager:topic-edit", topic_id=topic_id)
