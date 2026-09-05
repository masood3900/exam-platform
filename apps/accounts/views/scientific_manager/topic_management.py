from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.accounts.services.scientific_group_service import ScientificGroupService
from apps.assessments.models import ScientificGroup


class TopicManagementView(LoginRequiredMixin, View):
    """مدیریت موضوع‌های مدیر علمی"""

    template_name = "dashboard/scientific_manager/topic_management.html"

    def get(self, request):
        user = request.user

        # گروه‌هایی که مدیر علمی به آن‌ها متصل است
        managed_groups = ScientificGroupService.get_manager_fields(user)

        # والدهایی که می‌توانند موضوع جدید زیرشان ساخته شود
        available_parents = []
        # موضوع‌هایی که مدیر می‌تواند ببیند
        topics = []

        for group in managed_groups:
            if group.parent is None:
                # مدیر کل یک رشته → همه مسیرهای آموزشی زیرش
                available_parents.append(group)
                # مسیرهای آموزشی این رشته
                learning_paths = ScientificGroup.objects.filter(
                    parent=group,
                    is_active=True,
                )
                for lp in learning_paths:
                    if lp not in topics:
                        topics.append(lp)
                    # موضوع‌های زیر این مسیر آموزشی
                    sub_topics = ScientificGroup.objects.filter(
                        parent=lp,
                        is_active=True,
                    )
                    for st in sub_topics:
                        if st not in topics:
                            topics.append(st)
            else:
                # مدیر یک مسیر آموزشی → فقط موضوع‌های زیرش
                available_parents.append(group)
                sub_topics = ScientificGroup.objects.filter(
                    parent=group,
                    is_active=True,
                )
                for st in sub_topics:
                    if st not in topics:
                        topics.append(st)

        # QuerySet نهایی
        if topics:
            topics_query = ScientificGroup.objects.filter(
                id__in=[t.id for t in topics],
            ).prefetch_related("learning_objectives", "parent")
        else:
            topics_query = ScientificGroup.objects.none()

        return render(request, self.template_name, {
            "managed_groups": managed_groups,
            "available_parents": available_parents,
            "topics": topics_query,
        })


class TopicCreateView(LoginRequiredMixin, View):
    """ساخت موضوع جدید"""

    def post(self, request):
        name = request.POST.get("name", "").strip()
        code = request.POST.get("code", "").strip()
        description = request.POST.get("description", "").strip()
        parent_id = request.POST.get("parent_id")

        if not name or not code or not parent_id:
            messages.error(request, "نام، کد و والد الزامی است.")
            return redirect("accounts:scientific_manager:topic-management")

        try:
            ScientificGroupService.create_topic(
                name=name,
                code=code,
                description=description,
                parent_id=parent_id,
            )
            messages.success(request, f"موضوع «{name}» ساخته شد.")
        except Exception as e:
            messages.error(request, f"خطا در ساخت موضوع: {e}")

        return redirect("accounts:scientific_manager:topic-management")


class TopicDeleteView(LoginRequiredMixin, View):
    """حذف موضوع"""

    def post(self, request, topic_id):
        topic = get_object_or_404(ScientificGroup, id=topic_id)

        has_questions = topic.questions.exists()
        has_assessments = topic.assessments.exists()
        has_children = topic.children.exists()
        has_objectives = topic.learning_objectives.exists()

        if has_questions or has_assessments or has_children or has_objectives:
            messages.warning(
                request,
                f"موضوع «{topic.name}» قابل حذف نیست، زیرا "
                f"{'سوال' if has_questions else ''} "
                f"{'و' if has_questions and has_assessments else ''} "
                f"{'آزمون' if has_assessments else ''} "
                f"{'و' if (has_questions or has_assessments) and (has_children or has_objectives) else ''} "
                f"{'زیرموضوع' if has_children else ''} "
                f"{'و' if has_children and has_objectives else ''} "
                f"{'هدف آموزشی' if has_objectives else ''} "
                f"به آن متصل است.",
            )
        else:
            topic_name = topic.name
            topic.delete()
            messages.success(request, f"موضوع «{topic_name}» حذف شد.")

        return redirect("accounts:scientific_manager:topic-management")


class TopicToggleView(LoginRequiredMixin, View):
    """فعال/غیرفعال کردن موضوع"""

    def post(self, request, topic_id):
        topic = get_object_or_404(ScientificGroup, id=topic_id)
        topic.is_active = not topic.is_active
        topic.save(update_fields=["is_active"])

        status = "فعال" if topic.is_active else "غیرفعال"
        messages.success(request, f"موضوع «{topic.name}» {status} شد.")
        return redirect("accounts:scientific_manager:topic-management")
