import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.core.templatetags.markdown_extras import markdown_format
from apps.accounts.services.question_designer_dashboard_service import (
    QuestionDesignerDashboardService,
)


class QuestionDetailAPIView(LoginRequiredMixin, View):
    """نمایش جزئیات سوال به صورت JSON"""

    def get(self, request, question_id):

        question = QuestionDesignerDashboardService.get_question_details(
            user=request.user,
            question_id=question_id,
        )

        if not question:
            return JsonResponse({
                "error": "سوال یافت نشد"
            }, status=404)

        data = {
            "id": str(question.id),
            "code": question.code,
            "title": question.title,
            "body": markdown_format(question.body),
            "question_type": question.get_question_type_display(),
            "difficulty": question.get_difficulty_display(),
            "status": question.status,
            "status_display": question.get_status_display(),
            "score": str(question.score),
            "explanation": markdown_format(question.explanation) if question.explanation else "",
            "scientific_group": question.scientific_group.name if question.scientific_group else None,
            "reviewed_by": question.reviewed_by.get_full_name() if question.reviewed_by else None,
            "reviewed_at": question.reviewed_at.strftime("%Y-%m-%d %H:%M") if question.reviewed_at else None,
            "review_note": question.review_note,
            "choices": [
                {
                    "id": str(choice.id),
                    "text": choice.text,
                    "is_correct": choice.is_correct,
                    "explanation": choice.explanation,
                }
                for choice in question.choices.all()
            ],
            "review_history": [
                {
                    "action": history.get_action_display(),
                    "reviewer": history.reviewer.get_full_name() or history.reviewer.username,
                    "note": history.note,
                    "created_at": history.created_at.strftime("%Y-%m-%d %H:%M"),
                }
                for history in question.review_history.all()
            ],
        }

        return JsonResponse(data)