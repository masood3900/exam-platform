import uuid
from django.conf import settings
from django.db import models
from apps.assessments.models.question import(
    Question,
    Choice,
)
from apps.assessments.models.assessment import Assessment


class Attempt(models.Model):

    class Status(models.TextChoices):
        CREATED = "created", "Created"
        STARTED = "started", "Started"
        SUBMITTED = "submitted", "Submitted"
        GRADED = "graded", "Graded"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.PROTECT,
        related_name="attempts",
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assessment_attempts",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    # زمان واقعی پایان آزمون
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    current_question = models.PositiveSmallIntegerField(
        default=1,
    )

    total_questions = models.PositiveSmallIntegerField(
        default=0,
    )

    correct_answers = models.PositiveSmallIntegerField(
        default=0,
    )

    score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    passed = models.BooleanField(
        default=False,
    )

    # مدت زمان پاسخگویی (ثانیه)
    elapsed_seconds = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["-started_at"]

        indexes = [
            models.Index(fields=["student"]),
            models.Index(fields=["assessment"]),
            models.Index(fields=["status"]),
        ]

        verbose_name = "تلاش آزمون"
        verbose_name_plural = "تلاش‌های آزمون"

    def __str__(self):
        return f"{self.student} | {self.assessment.title}"
class AttemptQuestion(models.Model):

    class Status(models.TextChoices):
        NOT_VISITED = "not_visited", "بازدید نشده"
        VISITED = "visited", "بازدید شده"
        ANSWERED = "answered", "پاسخ داده شده"
        SKIPPED = "skipped", "رد شده"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    attempt = models.ForeignKey(
        Attempt,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        related_name="attempt_questions",
    )

    order = models.PositiveSmallIntegerField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_VISITED,
    )

    marked_for_review = models.BooleanField(
        default=False,
    )

    answered_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
    )

    is_correct = models.BooleanField(
        default=False,
    )

    class Meta:

        ordering = (
            "order",
        )

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "attempt",
                    "order",
                ],
                name="unique_attempt_question_order",
            ),

            models.UniqueConstraint(
                fields=[
                    "attempt",
                    "question",
                ],
                name="unique_attempt_question",
            ),

        ]

        indexes = [

            models.Index(
                fields=[
                    "attempt",
                    "order",
                ]
            ),

            models.Index(
                fields=[
                    "status",
                ]
            ),

        ]

        verbose_name = "سؤال آزمون"

        verbose_name_plural = "سؤال‌های آزمون"

    def __str__(self):

        return (
            f"{self.attempt.student} | "
            f"Q{self.order} | "
            f"{self.question.code}"
        )

class AttemptChoice(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    attempt_question = models.ForeignKey(
        AttemptQuestion,
        on_delete=models.CASCADE,
        related_name="choices",
    )

    original_choice = models.ForeignKey(
        Choice,
        on_delete=models.PROTECT,
        related_name="attempt_snapshots",
    )

    order = models.PositiveSmallIntegerField()

    text = models.TextField()

    is_correct = models.BooleanField(
        default=False,
    )

    explanation = models.TextField(
        blank=True,
    )

    selected = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "order",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "attempt_question",
                    "order",
                ],
                name="unique_attempt_choice_order",
            ),

            models.UniqueConstraint(
                fields=[
                    "attempt_question",
                    "original_choice",
                ],
                name="unique_attempt_original_choice",
            ),

        ]

        indexes = [

            models.Index(
                fields=[
                    "attempt_question",
                ]
            ),

            models.Index(
                fields=[
                    "selected",
                ]
            ),

        ]

        verbose_name = "گزینه آزمون"

        verbose_name_plural = "گزینه‌های آزمون"

    def __str__(self):

        return (
            f"{self.attempt_question.question.code} "
            f"- گزینه {self.order}"
        )