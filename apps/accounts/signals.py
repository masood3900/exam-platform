from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User, UserProfile
from apps.accounts.models_wallet import Wallet


@receiver(post_save, sender=User)
def create_user_related_objects(sender, instance, created, **kwargs):
    """ساخت خودکار کیف پول و پروفایل برای کاربر جدید"""
    if created:
        Wallet.objects.get_or_create(user=instance)
        UserProfile.objects.get_or_create(user=instance)
