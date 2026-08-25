import uuid
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.core.exceptions import ValidationError
from .course import Course
from .learning_path import LearningPath
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
        default=AssessmentType.PRACTICE,
        verbose_name="نوع آزمون",
    )

    description = models.TextField(
        blank=True,
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name="قیمت آزمون",
        help_text="قیمت پایه آزمون به تومان؛ صفر یعنی رایگان",
    )

    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
        ],
        verbose_name="درصد تخفیف",
        help_text="درصد تخفیف از 0 تا 100",
    )

    demo_attempts = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="تعداد تلاش آزمایشی",
        help_text="تعداد دفعاتی که کاربر قبل از خرید می‌تواند آزمون را آزمایش کند.",
    )
    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.PROTECT,
        related_name="assessments",
        null=True,
        blank=True,
        verbose_name="مسیر آموزشی",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="assessments",
        null=True,
        blank=True,
        verbose_name="دوره آموزشی",
    )
    objectives = models.ManyToManyField(
        "LearningObjective",
        related_name="assessments",
        blank=True,
        verbose_name="اهداف آموزشی",
    )
   
    duration_minutes = models.PositiveIntegerField(
        default=30,
    )

    passing_score = models.PositiveSmallIntegerField(
        default=70,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
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
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_assessments",   
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )
    @property
    def final_price(self):
        if self.price == 0:
            return 0

        return self.price * (
            100 - self.discount_percent
        ) // 100

    @property
    def is_free(self):
        return self.price == 0

    @property
    def has_discount(self):
        return (
            self.price > 0
            and self.discount_percent > 0
        )
    def clean(self):

        errors = {}

        # آزمون وابسته به دوره باید مسیر آموزشی داشته باشد
        if self.course and not self.learning_path:
            errors["learning_path"] = (
                "آزمونی که به یک دوره متصل است، "
                "باید مسیر آموزشی داشته باشد."
            )

        # اگر هر دو مشخص شده‌اند، باید متعلق به یک مسیر باشند
        if self.course and self.learning_path:

            if self.course.learning_path_id != self.learning_path_id:
                errors["learning_path"] = (
                    "مسیر آموزشی آزمون باید با مسیر آموزشی دوره یکسان باشد."
                )

        if errors:
            from django.core.exceptions import ValidationError
            raise ValidationError(errors)

    class Meta:
        ordering = ["assessment_type","title",]
        indexes =[
            models.Index(fields=["assessment_type",]),
            models.Index(fields=["is_active",]),
           
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
        verbose_name="آزمون",
    )

    category = models.ForeignKey(
        QuestionCategory,
        on_delete=models.PROTECT,
        related_name="assessment_rules",
        null=True,
        blank=True,
        verbose_name="دسته سوال",
    )

    learning_objective = models.ForeignKey(
        LearningObjective,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="assessment_rules",
        verbose_name="هدف آموزشی",
    )

    difficulty = models.CharField(
        max_length=20,
        choices=Question.Difficulty.choices,
        blank=True,
        null=True,
        verbose_name="سطح سختی",
    )

    question_count = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        verbose_name="تعداد سوال",
    )

    random_selection = models.BooleanField(
        default=True,
        verbose_name="انتخاب تصادفی سوالات",
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


    def clean(self):

        errors = {}

        # حداقل یکی از دسته یا هدف آموزشی باید مشخص باشد
        if not self.category and not self.learning_objective:
            errors["learning_objective"] = (
                "حداقل یک دسته یا هدف آموزشی باید انتخاب شود."
            )


        # بررسی ارتباط هدف آموزشی با دسته
        if self.learning_objective:

            if (
                self.category
                and self.learning_objective.category != self.category
            ):
                errors["learning_objective"] = (
                    "هدف آموزشی انتخاب شده متعلق به این دسته نیست."
                )


        # پیدا کردن سوالات قابل استفاده
        if self.learning_objective:

            questions = Question.objects.filter(
                learning_objective=self.learning_objective,
                is_active=True,
            )

        elif self.category:

            questions = Question.objects.filter(
                learning_objective__category=self.category,
                is_active=True,
            )

        else:

            questions = Question.objects.none()


        # اعمال فیلتر سطح سختی
        if self.difficulty:

            questions = questions.filter(
                difficulty=self.difficulty
            )


        available_count = questions.count()


        if self.question_count > available_count:

            errors["question_count"] = (
                f"تعداد درخواست شده بیشتر از سوالات موجود است. "
                f"تعداد موجود: {available_count}"
            )


        if errors:
            raise ValidationError(errors)



    def __str__(self):

        text = self.assessment.title


        if self.learning_objective:

            text += (
                f" | {self.learning_objective.code}"
            )

        elif self.category:

            text += (
                f" | {self.category.name}"
            )

        else:

            text += " | بدون دسته"


        text += (
            f" | {self.question_count} سؤال"
        )


        return text