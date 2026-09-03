from django.conf import settings
from django.db import models
from apps.messaging.validators import validate_message_file
from apps.education.models import InstructorAssignment
from apps.assessments.models import LearningPath


class Conversation(models.Model):
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="instructor_conversations", verbose_name="مدرس")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="student_conversations", verbose_name="دانش‌آموز")
    learning_path = models.ForeignKey(LearningPath, on_delete=models.PROTECT, related_name="conversations", verbose_name="مسیر آموزشی")
    assignment = models.OneToOneField(InstructorAssignment, on_delete=models.PROTECT, related_name="conversation", verbose_name="رابطه آموزشی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین تغییر")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "گفتگو"
        verbose_name_plural = "گفتگوها"

    def __str__(self):
        return f"{self.instructor} ↔ {self.student} | {self.learning_path.name}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages", verbose_name="گفتگو")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sent_messages", verbose_name="فرستنده")
    text = models.TextField(blank=True, verbose_name="متن پیام")
    file = models.FileField(upload_to="messaging/", validators=[validate_message_file], null=True, blank=True, verbose_name="فایل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ خواندن")

    class Meta:
        ordering = ["created_at"]
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"

    def __str__(self):
        return f"{self.sender} | {self.created_at:%Y-%m-%d %H:%M}"


class ConversationUserState(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="user_states")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversation_states")
    is_hidden = models.BooleanField(default=False)
    hidden_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["conversation", "user"], name="unique_conversation_user_state")]


class DirectMessage(models.Model):
    """پیام مستقیم بین هر دو کاربر"""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sent_direct_messages", verbose_name="فرستنده")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="received_direct_messages", verbose_name="گیرنده")
    subject = models.CharField(max_length=255, blank=True, verbose_name="موضوع")
    text = models.TextField(verbose_name="متن پیام")
    file = models.FileField(upload_to="direct_messages/", null=True, blank=True, verbose_name="فایل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ خواندن")
    is_archived_by_sender = models.BooleanField(default=False, verbose_name="بایگانی توسط فرستنده")
    is_archived_by_receiver = models.BooleanField(default=False, verbose_name="بایگانی توسط گیرنده")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "پیام مستقیم"
        verbose_name_plural = "پیام‌های مستقیم"

    def __str__(self):
        return f"{self.sender} → {self.receiver} | {self.created_at:%Y-%m-%d %H:%M}"


class Ticket(models.Model):
    """تیکت پشتیبانی"""

    class Status(models.TextChoices):
        OPEN = "open", "باز"
        IN_PROGRESS = "in_progress", "در حال بررسی"
        CLOSED = "closed", "بسته"

    class Priority(models.TextChoices):
        LOW = "low", "کم"
        NORMAL = "normal", "عادی"
        HIGH = "high", "زیاد"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets", verbose_name="کاربر")
    title = models.CharField(max_length=255, verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیحات")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, verbose_name="وضعیت")
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.NORMAL, verbose_name="اولویت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین تغییر")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت‌ها"

    def __str__(self):
        return f"#{self.id} - {self.title}"
