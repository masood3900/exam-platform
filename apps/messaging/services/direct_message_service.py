from django.db.models import Q
from django.utils import timezone

from apps.messaging.models import DirectMessage


class DirectMessageService:

    @staticmethod
    def send_message(*, sender, receiver, text, subject=""):
        """ارسال پیام مستقیم"""
        
        text = (text or "").strip()
        
        if not text:
            raise ValueError("پیام باید متن داشته باشد.")
        
        if sender.id == receiver.id:
            raise ValueError("نمی‌توانید به خودتان پیام بدهید.")
        
        message = DirectMessage.objects.create(
            sender=sender,
            receiver=receiver,
            subject=subject,
            text=text,
        )
        
        return message

    @staticmethod
    def get_inbox(user):
        """صندوق ورودی کاربر"""
        
        return DirectMessage.objects.filter(
            Q(receiver=user, is_archived_by_receiver=False) |
            Q(sender=user, is_archived_by_sender=False)
        ).select_related(
            "sender",
            "receiver",
        ).order_by("-created_at")

    @staticmethod
    def get_sent(user):
        """پیام‌های ارسال شده"""
        
        return DirectMessage.objects.filter(
            sender=user,
            is_archived_by_sender=False,
        ).select_related(
            "receiver",
        ).order_by("-created_at")

    @staticmethod
    def get_received(user):
        """پیام‌های دریافت شده"""
        
        return DirectMessage.objects.filter(
            receiver=user,
            is_archived_by_receiver=False,
        ).select_related(
            "sender",
        ).order_by("-created_at")

    @staticmethod
    def get_conversation(user, other_user):
        """گفتگوی بین دو کاربر"""
        
        return DirectMessage.objects.filter(
            Q(sender=user, receiver=other_user, is_archived_by_sender=False) |
            Q(sender=other_user, receiver=user, is_archived_by_receiver=False)
        ).select_related(
            "sender",
            "receiver",
        ).order_by("created_at")

    @staticmethod
    def mark_as_read(message, user):
        """علامت‌گذاری پیام به عنوان خوانده شده"""
        
        if message.receiver_id == user.id and not message.read_at:
            message.read_at = timezone.now()
            message.save(update_fields=["read_at"])

    @staticmethod
    def unread_count(user):
        """تعداد پیام‌های خوانده نشده"""
        
        return DirectMessage.objects.filter(
            receiver=user,
            read_at__isnull=True,
            is_archived_by_receiver=False,
        ).count()

    @staticmethod
    def archive(message, user):
        """بایگانی پیام"""
        
        if message.sender_id == user.id:
            message.is_archived_by_sender = True
            message.save(update_fields=["is_archived_by_sender"])
        elif message.receiver_id == user.id:
            message.is_archived_by_receiver = True
            message.save(update_fields=["is_archived_by_receiver"])