from django.db import transaction

from apps.assessments.models import (
    Question,
    QuestionReviewHistory,
)


class QuestionService:
    """سرویس مدیریت سوالات"""

    @staticmethod
    def bulk_submit(question_ids, user):
        """ارسال گروهی سوالات برای تایید"""
        questions = Question.objects.filter(
            id__in=question_ids,
            status__in=[Question.QuestionStatus.DRAFT, Question.QuestionStatus.REJECTED],
        )

        count = 0
        for question in questions:
            question.status = Question.QuestionStatus.PENDING
            question.save(update_fields=["status"])

            QuestionReviewHistory.objects.create(
                question=question,
                reviewer=user,
                action=QuestionReviewHistory.Action.SUBMIT,
            )
            count += 1

        return count

    @staticmethod
    def bulk_review(question_ids, reviewer, action, note=""):
        """تایید/رد گروهی سوالات"""
        questions = Question.objects.filter(
            id__in=question_ids,
            status=Question.QuestionStatus.PENDING,
        )

        new_status = (
            Question.QuestionStatus.APPROVED
            if action == "approve"
            else Question.QuestionStatus.REJECTED
        )

        count = 0
        for question in questions:
            question.status = new_status
            question.reviewed_by = reviewer
            question.review_note = note
            question.is_active = (action == "approve")
            question.save()

            QuestionReviewHistory.objects.create(
                question=question,
                reviewer=reviewer,
                action=action,
                note=note,
            )
            count += 1

        return count

    @staticmethod
    def update_question_with_choices(question, form, formset):
        """
        به‌روزرسانی سوال به همراه گزینه‌های آن
        
        Args:
            question: نمونه Question
            form: فرم QuestionForm معتبر
            formset: فرم‌ست ChoiceFormSet معتبر
        
        Returns:
            question: سوال به‌روزرسانی شده
        """
        with transaction.atomic():
            # ذخیره اطلاعات اصلی سوال
            question = form.save(commit=False)
            question.scientific_group = form.cleaned_data["topic"]
            question.learning_objective = form.cleaned_data["learning_objective"]
            question.save()

            # ذخیره گزینه‌ها با order خودکار
            choices = formset.save(commit=False)
            for index, choice in enumerate(choices):
                choice.order = index
                choice.save()

            # حذف گزینه‌های حذف‌شده
            for obj in formset.deleted_objects:
                obj.delete()

        return question