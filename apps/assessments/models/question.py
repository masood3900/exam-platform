import uuid
from django.conf import settings
from django.db import models


class QuestionCategory(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )
    department = models.ForeignKey(
        "core.Department",
        on_delete=models.PROTECT,
        related_name="question_categories",
        verbose_name="دپارتمان",
        null=True,
        blank=True,
    )


    description = models.TextField(

        blank=True,
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
    )

    order = models.PositiveIntegerField(
        default=0,
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
        ordering = ["order", "name"]
        indexes = [
            models.Index(fields=["parent"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["order"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["department","parent", "name"],
                name="unique_category_name_per_parent",
            ),
        ]
        verbose_name = "دسته سوال"
        verbose_name_plural = "دسته‌بندی سوالات"
    @property
    def level(self):
        level = 0
        parent = self.parent

        while parent:
            level += 1
            parent = parent.parent

        return level
    @property
    def has_children(self):
        return self.children.exists()
    @property
    def full_name(self):

        if self.parent:
            return f"{self.parent.full_name} > {self.name}"
        return self.name

    def __str__(self):
        return self.name

class LearningObjective(models.Model):

    class BloomLevel(models.TextChoices):
        REMEMBER = "remember", "Remember"
        UNDERSTAND = "understand", "Understand"
        APPLY = "apply", "Apply"
        ANALYZE = "analyze", "Analyze"
        EVALUATE = "evaluate", "Evaluate"
        CREATE = "create", "Create"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    code = models.CharField(
        max_length=30,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
    )

    category = models.ForeignKey(
        QuestionCategory,
        on_delete=models.PROTECT,
        related_name="learning_objectives",
    )

    weight = models.PositiveSmallIntegerField(
        default=1,
        help_text="اهمیت این هدف آموزشی در تحلیل یادگیری",
    )

    bloom_level = models.CharField(
        max_length=20,
        choices=BloomLevel.choices,
        default=BloomLevel.UNDERSTAND,
    )

    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
    )

    estimated_minutes = models.PositiveSmallIntegerField(
        default=15,
        help_text="زمان تقریبی یادگیری این مبحث",
    )

    order = models.PositiveIntegerField(
        default=1,
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
        ordering = ["category", "order", "code"]
        verbose_name = "هدف آموزشی"
        verbose_name_plural = "اهداف آموزشی"

    def __str__(self):
        return f"{self.code} - {self.name}"
class Question(models.Model):

    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = "mcq", "چهار گزینه‌ای"
        TRUE_FALSE = "tf", "صحیح / غلط"
        MULTI_SELECT = "msq", "چند گزینه‌ای"
        SHORT_ANSWER = "short", "پاسخ کوتاه"
        CODING = "code", "کدنویسی"

    class Difficulty(models.TextChoices):
        EASY = "easy", "آسان"
        MEDIUM = "medium", "متوسط"
        HARD = "hard", "سخت"

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
        blank=True,
    )

    body = models.TextField()

    learning_objective = models.ForeignKey(
        LearningObjective,
        on_delete=models.PROTECT,
        related_name="questions",
    )

    question_type = models.CharField(
        max_length=20,
        choices=QuestionType.choices,
        default=QuestionType.MULTIPLE_CHOICE,
    )

    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
    )

    estimated_seconds = models.PositiveSmallIntegerField(
        default=60,
        help_text="زمان تقریبی پاسخ (ثانیه)",
    )

    correct_answers_required = models.PositiveSmallIntegerField(
        default=1,
    )

    explanation = models.TextField(
        blank=True,
        help_text="توضیحی که بعد از پاسخ صحیح نمایش داده می‌شود.",
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
        ordering = [
            "learning_objective",
            "code",
        ]
        verbose_name = "سؤال"
        verbose_name_plural = "بانک سؤالات"
        indexes = [
            models.Index(fields=["learning_objective"]),
            models.Index(fields=["difficulty"]),
            models.Index(fields=["is_active"]),
        ]

    @property
    def choices_count(self):
        return self.choices.count()

    @property
    def correct_choices_count(self):
        return self.choices.filter(
            is_correct=True,
        ).count()
    @property
    def is_complete(self):

        if self.choices_count < 2:
            return False

        if self.correct_choices_count != self.correct_answers_required:
            return False

        return True

    def __str__(self):
        if self.title:
            return f"{self.code} - {self.title}"
        return self.code
class Choice(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="choices",
    )

    text = models.TextField()

    order = models.PositiveSmallIntegerField(
        default=0,
    )

    is_correct = models.BooleanField(
        default=False,
    )

    explanation = models.TextField(
        blank=True,
        help_text="در صورت نیاز، توضیح اختصاصی برای این گزینه",
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

        ordering = [
            "question",
            "order",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "question",
                    "order",
                ],
                name="unique_choice_order_per_question",
            )
        ]

        indexes = [
            models.Index(
                fields=[
                    "question",
                ]
            ),

            models.Index(
                fields=[
                    "is_correct",
                ]
            ),
        ]

        verbose_name = "گزینه"
        verbose_name_plural = "گزینه‌های سؤال"


    @property
    def label(self):

        labels = {
            1: "الف",
            2: "ب",
            3: "ج",
            4: "د",
            5: "هـ",
            6: "و",
        }

        return labels.get(
            self.order,
            str(self.order),
        )


    def __str__(self):

        return f"{self.question.code} - گزینه {self.order}"