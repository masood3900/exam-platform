from django.db import transaction
from django.utils import timezone

from apps.assessments.models import Attempt
from apps.assessments.services import QuestionSelectorService


class AttemptService:

    @staticmethod
    @transaction.atomic
    def start_attempt(
        student,
        assessment,
    ):

        if not assessment.is_active:
            raise ValueError(
                "این آزمون غیرفعال است."
            )

        previous_attempts = Attempt.objects.filter(
            student = student,
            assessment = assessment,
        ).exclude(
            status = Attempt.Status.CANCELLED,
        ).count()
        if previous_attempts >= assessment.max_attempts:
            raise ValueError(
                "تعداد دفعات مجاز شرکت در این آزمون تمام شده است."
            )


        attempt = QuestionSelectorService.generate_attempt(
            assessment=assessment,
            student=student,
        )

        attempt.status = Attempt.Status.STARTED
        attempt.started_at = timezone.now()

        attempt.save(
            update_fields=[
                "status",
                "started_at",
            ]
        )

        return attempt


    @staticmethod
    @transaction.atomic
    def submit_answer(
        attempt,
        attempt_question,
        selected_choice_ids,
    ):

        if attempt_question.attempt != attempt:
            raise ValueError(
                "این سؤال متعلق به این آزمون نیست."
            )

        # حذف انتخاب‌های قبلی
        attempt_question.choices.update(
            selected=False
        )

        # انتخاب گزینه جدید
        attempt_question.choices.filter(
            id__in=selected_choice_ids
        ).update(
            selected=True
        )


    @staticmethod
    @transaction.atomic
    def check_answer(
        attempt,
        attempt_question,
    ):

        if attempt_question.attempt != attempt:
            raise ValueError(
                "این سؤال متعلق به این آزمون نیست."
            )

        if attempt_question.is_answered:
            raise ValueError(
                "این سؤال قبلاً بررسی شده است."
            )


        selected_choices = (
            attempt_question.choices
            .filter(
                selected=True,
            )
        )


        if not selected_choices.exists():
            raise ValueError(
                "برای این سؤال پاسخی انتخاب نشده است."
            )


        correct = True


        for choice in attempt_question.choices.all():

            if choice.selected != choice.is_correct:
                correct = False
                break


        if correct:

            score = attempt_question.score

            attempt.correct_answers += 1

        else:

            score = 0


        attempt_question.is_answered = True

        attempt_question.save(
            update_fields=[
                "is_answered",
            ]
        )


        attempt.save(
            update_fields=[
                "correct_answers",
            ]
        )


        return {
            "correct": correct,
            "score": score,
        }


    @staticmethod
    @transaction.atomic
    def finish_attempt(
        attempt,
    ):

        if attempt.status != Attempt.Status.STARTED:
            raise ValueError(
                "این آزمون قابل پایان دادن نیست."
            )


        unanswered = (
            attempt.questions
            .filter(
                is_answered=False,
            )
            .exists()
        )


        if unanswered:
            raise ValueError(
                "همه سوالات پاسخ داده نشده‌اند."
            )


        total_score = 0


        for question in attempt.questions.all():

            if question.choices.filter(
                selected=True,
                is_correct=True,
            ).exists():

                total_score += question.score


        max_score = sum(
            question.score
            for question in attempt.questions.all()
        )


        percentage = 0


        if max_score:

            percentage = (
                total_score / max_score
            ) * 100


        attempt.score = total_score

        attempt.percentage = percentage

        attempt.passed = (
            percentage >= attempt.assessment.passing_score
        )

        attempt.status = Attempt.Status.GRADED

        attempt.submitted_at = timezone.now()


        attempt.save(
            update_fields=[
                "score",
                "percentage",
                "passed",
                "status",
                "submitted_at",
            ]
        )


        return attempt