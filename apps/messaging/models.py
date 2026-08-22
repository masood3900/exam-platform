from django.conf import settings
from django.db import models
from apps.messaging.validators import validate_message_file
from apps.education.models import InstructorAssignment
from apps.assessments.models import LearningPath


class Conversation(models.Model):

    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="instructor_conversations",
        verbose_name="مدرس",
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="student_conversations",
        verbose_name="دانش‌آموز",
    )

    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.PROTECT,
        related_name="conversations",
        verbose_name="مسیر آموزشی",
    )

    assignment = models.OneToOneField(
        InstructorAssignment,
        on_delete=models.PROTECT,
        related_name="conversation",
        verbose_name="رابطه آموزشی",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین تغییر",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
    )

    class Meta:
        ordering = ["-updated_at"]

        verbose_name = "گفتگو"
        verbose_name_plural = "گفتگوها"

        indexes = [
            models.Index(
                fields=["instructor", "student"],
            ),
            models.Index(
                fields=["learning_path"],
            ),
            models.Index(
                fields=["is_active"],
            ),
        ]

    def __str__(self):
        return (
            f"{self.instructor} ↔ "
            f"{self.student} | "
            f"{self.learning_path.name}"
        )

    
class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="گفتگو",
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="sent_messages",
        verbose_name="فرستنده",
    )

    text = models.TextField(
        blank=True,
        verbose_name="متن پیام",
    )
    file = models.FileField(
        upload_to="messaging/",
        validators=[validate_message_file],
        null=True,
        blank=True,
        verbose_name="فایل",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ارسال",
    )

    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ خواندن",
    )

    class Meta:
        ordering = ["created_at"]

        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"

        indexes = [
            models.Index(
                fields=["conversation", "created_at"],
            ),
            models.Index(
                fields=["sender"],
            ),
            models.Index(
                fields=["read_at"],
            ),
        ]

    def __str__(self):
        return (
            f"{self.sender} | "
            f"{self.created_at:%Y-%m-%d %H:%M}"
        )
class ConversationUserState(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="user_states",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversation_states",
    )

    is_hidden = models.BooleanField(
        default=False,
    )

    hidden_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["conversation", "user"],
                name="unique_conversation_user_state",
            ),
        ]