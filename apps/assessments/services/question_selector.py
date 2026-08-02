import random

from django.db import transaction

from apps.assessments.models import (
    Assessment,
    Attempt,
    AssessmentRule,
    AttemptChoice,
    AttemptQuestion,
    Question,
)


class QuestionSelectorService:

    @classmethod
    @transaction.atomic
    def generate_attempt(
        cls,
        assessment: Assessment,
        student,
    ):

        attempt = Attempt.objects.create(
            assessment=assessment,
            student=student,
            status=Attempt.Status.CREATED,
        )

        questions = cls._select_questions(
            assessment,
        )

        cls._create_attempt_questions(
            attempt=attempt,
            questions=questions,
        )

        attempt.total_questions = len(questions)

        attempt.save(
            update_fields=[
                "total_questions",
            ]
        )

        return attempt

    @classmethod
    def _select_questions(
        cls,
        assessment: Assessment,
    ):

        selected_questions = []

        rules = (
            AssessmentRule.objects
            .filter(
                assessment=assessment,
            )
            .select_related(
                "category",
                "learning_objective",
            )
        )

        for rule in rules:

            queryset = (
                Question.objects
                .filter(
                    is_active=True,
                    learning_objective__category=rule.category,
                )
            )

            if rule.learning_objective:

                queryset = queryset.filter(
                    learning_objective=rule.learning_objective,
                )

            if rule.difficulty:

                queryset = queryset.filter(
                    difficulty=rule.difficulty,
                )

            questions = list(queryset)

            if len(questions) < rule.question_count:

                raise ValueError(
                    f"بانک سؤال برای قانون «{rule}» کافی نیست."
                )

            random.shuffle(questions)

            selected_questions.extend(
                questions[: rule.question_count]
            )

        if assessment.shuffle_questions:
            random.shuffle(selected_questions)

        return selected_questions

    @classmethod
    def _create_attempt_questions(
        cls,
        *,
        attempt,
        questions,
    ):

        for order, question in enumerate(
            questions,
            start=1,
        ):

            attempt_question = AttemptQuestion.objects.create(
                attempt=attempt,
                original_question=question,
                order=order,
                code=question.code,
                title=question.title,
                body=question.body,
                explanation=question.explanation,
                question_type=question.question_type,
                difficulty=question.difficulty,
                score=question.score,
                correct_answers_required=question.correct_answers_required,
                estimated_seconds=question.estimated_seconds,
            )

            cls._create_attempt_choices(
                attempt_question=attempt_question,
                question=question,
            )

    @classmethod
    def _create_attempt_choices(
        cls,
        *,
        attempt_question,
        question,
    ):

        choices = list(
            question.choices
            .filter(
                is_active=True,
            )
            .order_by(
                "order",
            )
        )

        if attempt_question.attempt.assessment.shuffle_choices:
            random.shuffle(choices)

        for order, choice in enumerate(
            choices,
            start=1,
        ):

            AttemptChoice.objects.create(
                attempt_question=attempt_question,
                original_choice=choice,
                order=order,
                text=choice.text,
                is_correct=choice.is_correct,
                explanation=choice.explanation,
            )