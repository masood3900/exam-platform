from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db import models

from apps.messaging.models import (
    Conversation,
    ConversationUserState,
    Message,
)


class MessagingService:

    @staticmethod
    def can_access_conversation(
        conversation,
        user,
    ):
        return (
            conversation.instructor_id == user.id
            or conversation.student_id == user.id
        )

    @staticmethod
    def get_conversation(
        conversation_id,
        user,
    ):
        conversation = (
            Conversation.objects
            .select_related(
                "instructor",
                "student",
                "learning_path",
                "assignment",
            )
            .get(
                id=conversation_id,
            )
        )

        if not MessagingService.can_access_conversation(
            conversation,
            user,
        ):
            raise PermissionDenied(
                "شما عضو این گفتگو نیستید."
            )

        return conversation

    @staticmethod
    def send_message(
        conversation,
        sender,
        text="",
        file=None,
    ):
        if not MessagingService.can_access_conversation(
            conversation,
            sender,
        ):
            raise PermissionDenied(
                "شما عضو این گفتگو نیستید."
            )

        text = (text or "").strip()

        if not text and not file:
            raise ValueError(
                "پیام باید حداقل متن یا فایل داشته باشد."
            )
        
        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            text=text,
            file=file,
        )

        # اگر گفتگو قبلاً برای فرستنده مخفی شده بود،
        # با ارسال پیام دوباره در صندوق او ظاهر شود.
        ConversationUserState.objects.filter(
            conversation=conversation,
            user=sender,
        ).update(
            is_hidden=False,
            hidden_at=None,
        )

        return message

    @staticmethod
    def get_messages(
        conversation,
        user,
    ):
        if not MessagingService.can_access_conversation(
            conversation,
            user,
        ):
            raise PermissionDenied(
                "شما عضو این گفتگو نیستید."
            )

        return (
            conversation.messages
            .select_related("sender")
            .order_by("created_at")
        )

    @staticmethod
    def get_or_create_conversation(
        student,
        instructor,
        learning_path,
        assignment,
    ):
        conversation, created = (
            Conversation.objects.get_or_create(
                assignment=assignment,
                defaults={
                    "student": student,
                    "instructor": instructor,
                    "learning_path": learning_path,
                },
            )
        )

        return conversation

    @staticmethod
    def hide_conversation(
        conversation,
        user,
    ):
        if not MessagingService.can_access_conversation(
            conversation,
            user,
        ):
            raise PermissionDenied(
                "شما عضو این گفتگو نیستید."
            )

        (
            ConversationUserState.objects
            .update_or_create(
                conversation=conversation,
                user=user,
                defaults={
                    "is_hidden": True,
                    "hidden_at": timezone.now(),
                },
            )
        )

    @staticmethod
    def is_hidden_for_user(
        conversation,
        user,
    ):
        return (
            ConversationUserState.objects
            .filter(
                conversation=conversation,
                user=user,
                is_hidden=True,
            )
            .exists()
        )

    @staticmethod
    def get_inbox(
        user,
    ):

        hidden_conversation_ids = (
            ConversationUserState.objects
            .filter(
                user=user,
                is_hidden=True,
            )
            .values(
                "conversation_id",
            )
        )

        conversations = (
            Conversation.objects
            .filter(
                is_active=True,
            )
            .filter(
                models.Q(
                    instructor=user,
                )
                |
                models.Q(
                    student=user,
                )
            )
            .exclude(
                id__in=hidden_conversation_ids,
            )
            .annotate(
                unread_count=models.Count(
                    "messages",
                    filter=(
                        models.Q(
                            messages__read_at__isnull=True,
                        )
                        & ~models.Q(
                            messages__sender=user,
                        )
                    ),
                ),
            )
            .select_related(
                "instructor",
                "student",
                "learning_path",
            )
            .prefetch_related(
                models.Prefetch(
                    "messages",
                    queryset=(
                        Message.objects
                        .select_related("sender")
                        .order_by("-created_at")
                    ),
                    to_attr="inbox_messages",
                )
            )
            .order_by(
                "-updated_at",
            )
        )

        return conversations
    
    @staticmethod
    def get_message(
        message_id,
        user,
    ):

        message = (
            Message.objects
            .select_related(
                "conversation",
                "conversation__instructor",
                "conversation__student",
            )
            .get(
                id=message_id,
            )
        )

        if not MessagingService.can_access_conversation(
            message.conversation,
            user,
        ):
            raise PermissionDenied(
                "شما به این فایل دسترسی ندارید."
            )

        return message
    @staticmethod
    def get_unread_message_count(user):
        return (
            Message.objects
            .filter(
                conversation__is_active=True,
                read_at__isnull=True,
            )
            .exclude(
                sender=user,
            )
            .filter(
                conversation__instructor=user,
            )
            .count()
            +
            Message.objects
            .filter(
                conversation__is_active=True,
                read_at__isnull=True,
            )
            .exclude(
                sender=user,
            )
            .filter(
                conversation__student=user,
            )
            .count()
        )
    
    @staticmethod
    def mark_messages_as_read(
        conversation,
        user,
    ):
        if not MessagingService.can_access_conversation(
            conversation,
            user,
        ):
            raise PermissionDenied(
                "شما عضو این گفتگو نیستید."
            )

        other_user_id = (
            conversation.student_id
            if user.id == conversation.instructor_id
            else conversation.instructor_id
        )

        return (
            Message.objects
            .filter(
                conversation=conversation,
                sender_id=other_user_id,
                read_at__isnull=True,
            )
            .update(
                read_at=timezone.now(),
            )
        )