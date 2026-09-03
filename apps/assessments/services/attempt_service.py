import random

from django.db import transaction
from django.utils import timezone

from apps.assessments.models import (
    Attempt,
    AttemptQuestion,
    AttemptChoice,
    Question,
    AssessmentEnrollment,
)


class AttemptService:

    @staticmethod
    def can_start_attempt(
        *,
        student,
        assessment,
    ):
        """
        بررسی امکان شروع آزمون.

        آزمون رایگان:
        بر اساس max_attempts

        آزمون پولی با Enrollment فعال:
        بر اساس max_attempts

        آزمون پولی بدون خرید:
        فقط به تعداد demo_attempts
        """
        if not assessment.is_active:
            return False

        if student.is_superuser:
            return True

        attempts = Attempt.objects.filter(
            student=student,
            assessment=assessment,
            status__in=[
                Attempt.Status.STARTED,
                Attempt.Status.GRADED,
            ],
        ).count()

        if assessment.is_free:
            return True  # بی‌نهایت

        enrollment = assessment.enrollments.filter(
            user=student,
            status=AssessmentEnrollment.Status.ACTIVE,
        ).first()

        if enrollment and enrollment.payment_status == AssessmentEnrollment.PaymentStatus.PAID:
            return True  # پرداخت شده = بی‌نهایت

        # چک PaymentRequest تایید شده
        from apps.assessments.models import PaymentRequest
        has_paid = PaymentRequest.objects.filter(
            user=student,
            assessment=assessment,
            status="approved",
        ).exists()
        
        if has_paid:
            return True

        return attempts < assessment.demo_attempts

    @staticmethod
    @transaction.atomic
    def start_attempt(
        *,
        student,
        assessment,
    ):
        """
        ایجاد یک Attempt جدید
        انتخاب سوالات
        ساخت Snapshot سوال و گزینه‌ها
        """

        if not AttemptService.can_start_attempt(
            student=student,
            assessment=assessment,
        ):
            raise ValueError(
                "تعداد دفعات مجاز شرکت در این آزمون تمام شده است."
            )

        attempt = Attempt.objects.create(
            assessment=assessment,
            student=student,
            status=Attempt.Status.STARTED,
            started_at=timezone.now(),
        )

        questions = AttemptService._select_questions(
            assessment=assessment,
        )

        AttemptService._create_attempt_questions(
            attempt=attempt,
            questions=questions,
            shuffle_choices=assessment.shuffle_choices,
        )

        attempt.total_questions = len(questions)

        attempt.save(
            update_fields=[
                "total_questions",
            ]
        )

        return attempt

    @staticmethod
    def _select_questions(
        *,
        assessment,
    ):
        """
        انتخاب سوالات بر اساس Ruleها
        """

        selected_questions = []

        rules = assessment.rules.select_related(
            "category",
            "learning_objective",
        )

        for rule in rules:

            queryset = AttemptService._build_question_queryset(
                rule=rule,
            )

            questions = list(queryset)

            if len(questions) < rule.question_count:

                raise ValueError(
                    f"سوال کافی برای قانون "
                    f"{rule}"
                    f" وجود ندارد."
                )

            if rule.random_selection:
                random.shuffle(questions)

            selected_questions.extend(
                questions[:rule.question_count]
            )

        if assessment.shuffle_questions:
            random.shuffle(selected_questions)

        return selected_questions

    @staticmethod
    def _build_question_queryset(
        *,
        rule,
    ):
        """
        ساخت QuerySet سوالات بر اساس Rule
        """

        queryset = Question.objects.filter(
            is_active=True,
        ).select_related(
            "learning_objective",
            "learning_objective__category",
        )

        if rule.category:

            queryset = queryset.filter(
                learning_objective__category=rule.category,
            )

        if rule.learning_objective:

            queryset = queryset.filter(
                learning_objective=rule.learning_objective,
            )

        if rule.difficulty:

            queryset = queryset.filter(
                difficulty=rule.difficulty,
            )

        queryset = queryset.prefetch_related(
            "choices",
        )

        return queryset

    @staticmethod
    @transaction.atomic
    def _create_attempt_questions(
        *,
        attempt,
        questions,
        shuffle_choices=False,
    ):
        """
        ساخت Snapshot سوال و گزینه‌ها
        """

        for order, question in enumerate(
            questions,
            start=1,
        ):

            attempt_question = AttemptQuestion.objects.create(
                attempt=attempt,
                question=question,
                order=order,
            )

            choices = list(
                question.choices.filter(
                    is_active=True,
                )
            )

            if shuffle_choices:
                random.shuffle(choices)

            for index, choice in enumerate(
                choices,
                start=1,
            ):

                AttemptChoice.objects.create(
                    attempt_question=attempt_question,
                    original_choice=choice,
                    order=index,
                    text=choice.text,
                    is_correct=choice.is_correct,
                    explanation=choice.explanation,
                )

    @staticmethod
    @transaction.atomic
    def submit_answer(
        *,
        attempt,
        attempt_question,
        selected_choice_ids,
    ):
        """
        ثبت پاسخ دانشجو
        """

        if attempt.status != Attempt.Status.STARTED:
            raise ValueError(
                "این آزمون فعال نیست."
            )

        if attempt_question.attempt != attempt:
            raise ValueError(
                "این سؤال متعلق به این آزمون نیست."
            )

        attempt_question.choices.update(
            selected=False,
        )

        attempt_question.choices.filter(
            id__in=selected_choice_ids,
        ).update(
            selected=True,
        )

        attempt_question.status = (
            AttemptQuestion.Status.ANSWERED
        )

        attempt_question.answered_at = (
            timezone.now()
        )

        attempt_question.save(
            update_fields=[
                "status",
                "answered_at",
            ]
        )

    @staticmethod
    @transaction.atomic
    def check_answer(
        *,
        attempt,
        attempt_question,
    ):
        """
        تصحیح پاسخ سؤال
        """

        if attempt_question.attempt != attempt:
            raise ValueError(
                "این سؤال متعلق به این آزمون نیست."
            )

        selected_choices = list(
            attempt_question.choices.filter(
                selected=True,
            )
        )

        if not selected_choices:
            raise ValueError(
                "هیچ گزینه‌ای انتخاب نشده است."
            )

        correct_choices = list(
            attempt_question.choices.filter(
                is_correct=True,
            )
        )

        selected_ids = {
            choice.id
            for choice in selected_choices
        }

        correct_ids = {
            choice.id
            for choice in correct_choices
        }

        is_correct = (
            selected_ids == correct_ids
        )

        attempt_question.is_correct = is_correct

        if is_correct:
            attempt_question.score = (
                attempt_question.question.score
            )
        else:
            attempt_question.score = 0

        attempt_question.save(
            update_fields=[
                "is_correct",
                "score",
            ]
        )

        return is_correct

    @staticmethod
    @transaction.atomic
    def finalize_unanswered_questions(
        attempt,
    ):
        """
        سوالات بدون پاسخ را نهایی می‌کند.
        """

        unanswered = attempt.questions.exclude(
            status=AttemptQuestion.Status.ANSWERED,
        )

        for question in unanswered:

            question.is_correct = False
            question.score = 0
            question.status = (
                AttemptQuestion.Status.SKIPPED
            )

            question.save(
                update_fields=[
                    "is_correct",
                    "score",
                    "status",
                ]
            )

    @staticmethod
    @transaction.atomic
    def finish_attempt(
        attempt,
    ):
        """
        پایان آزمون
        محاسبه نمره و درصد
        """

        if attempt.status != Attempt.Status.STARTED:
            raise ValueError(
                "این آزمون قابل پایان دادن نیست."
            )

        AttemptService.finalize_unanswered_questions(
            attempt,
        )

        total_score = sum(
            question.score or 0
            for question in attempt.questions.all()
        )

        max_score = sum(
            question.question.score
            for question in attempt.questions.all()
        )

        percentage = 0

        if max_score:
            percentage = round(
                (total_score / max_score) * 100,
                2,
            )

        passed = (
            percentage >= attempt.assessment.passing_score
        )

        attempt.score = total_score

        attempt.percentage = percentage

        attempt.correct_answers = (
            attempt.questions.filter(
                is_correct=True,
            ).count()
        )

        attempt.passed = passed

        attempt.status = Attempt.Status.GRADED

        attempt.submitted_at = timezone.now()

        attempt.finished_at = timezone.now()

        attempt.save(
            update_fields=[
                "score",
                "percentage",
                "correct_answers",
                "passed",
                "status",
                "submitted_at",
                "finished_at",
            ]
        )

        return attempt