import uuid
from django.conf import settings
from django.db import models
from apps.assessments.models.question import(
    QuestionCategory,
    LearningObjective,
    Question,
)



class Assessment(models.Model):

    class AssessmentType(models.TextChoices):
        LEVEL = "level", "تعیین سطح"
        PRACTICE = "practice", "تمرین"
        HOMEWORK = "homework", "تکلیف"
        FINAL = "final", "پایان دوره"
        RETRY = "retry", "آزمون مجدد"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    code = models.CharField(
        max_length=30,
        unique=True,
    )

    title = models.CharField(
        max_length=255,
    )

    assessment_type = models.CharField(
        max_length=20,
        choices=AssessmentType.choices,
    )

    description = models.TextField(
        blank=True,
    )

    duration_minutes = models.PositiveIntegerField(
        default=30,
    )

    passing_score = models.PositiveSmallIntegerField(
        default=70,
        help_text="حداقل درصد قبولی",
    )

    max_attempts = models.PositiveSmallIntegerField(
        default=1,
    )

    shuffle_questions = models.BooleanField(
        default=True,
    )

    shuffle_choices = models.BooleanField(
        default=True,
    )

    show_result_immediately = models.BooleanField(
        default=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["assessment_type","title"]
        indexes =[
            models.Index(fields=["assessment_type"]),
            models.Index(fields=["is_active"]),
        ]
        verbose_name = "آزمون"
        verbose_name_plural = "آزمون‌ها"

    @property
    def total_questions(self):
        return sum(
            rule.question_count
            for rule in self.rules.all()
        )

    def __str__(self):
        return self.title

class AssessmentRule(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="rules",
    )

    category = models.ForeignKey(
        QuestionCategory,
        on_delete=models.PROTECT,
        related_name="assessment_rules",
    )

    learning_objective = models.ForeignKey(
        LearningObjective,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="assessment_rules",
    )

    difficulty = models.CharField(
        max_length=20,
        choices=Question.Difficulty.choices,
        blank=True,
        null=True,
    )

    question_count = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        ordering = [
            "assessment",
            "category",
            "learning_objective",
        ]
        constraints = [
            models.UniqueConstraint(
            fields=[
                "assessment",
                "category",
                "learning_objective",
                "difficulty",
            ],
            name="unique_assessment_rule",
        ),
    ]

        verbose_name = "قانون انتخاب سؤال"
        verbose_name_plural = "قوانین انتخاب سؤال"

    def __str__(self):

        text = self.assessment.title

        if self.learning_objective:
            text += f" | {self.learning_objective.code}"
        else:
            text += f" | {self.category.name}"

        text += f" | {self.question_count} سؤال"

        return text
