from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from apps.accounts.models import User
from apps.messaging.models import DirectMessage
from apps.messaging.services.direct_message_service import DirectMessageService


class DirectInboxView(LoginRequiredMixin, View):
    """صندوق ورودی پیام‌های مستقیم"""

    template_name = "messaging/direct_inbox.html"

    def get(self, request):
        inbox = DirectMessageService.get_inbox(request.user)
        unread_count = DirectMessageService.unread_count(request.user)
        
        return render(request, self.template_name, {
            "inbox": inbox,
            "unread_count": unread_count,
        })


class DirectComposeView(LoginRequiredMixin, View):
    """ارسال پیام جدید"""

    template_name = "messaging/direct_compose.html"

    def get(self, request):
        # لیست کاربران برای انتخاب گیرنده
        users = User.objects.filter(
            is_active=True,
        ).exclude(
            id=request.user.id,
        ).order_by("first_name", "last_name")
        
        return render(request, self.template_name, {
            "users": users,
        })

    def post(self, request):
        receiver_id = request.POST.get("receiver")
        subject = request.POST.get("subject", "")
        text = request.POST.get("text", "")
        
        receiver = get_object_or_404(User, id=receiver_id)
        
        try:
            DirectMessageService.send_message(
                sender=request.user,
                receiver=receiver,
                text=text,
                subject=subject,
            )
            messages.success(request, "پیام ارسال شد.")
            return redirect("messaging:direct-inbox")
        except ValueError as exc:
            messages.error(request, str(exc))
            return redirect("messaging:direct-compose")


class DirectConversationView(LoginRequiredMixin, View):
    """گفتگو با یک کاربر"""

    template_name = "messaging/direct_conversation.html"

    def get(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)
        conversation = DirectMessageService.get_conversation(request.user, other_user)
        
        # علامت‌گذاری پیام‌های دریافتی به عنوان خوانده شده
        for message in conversation:
            DirectMessageService.mark_as_read(message, request.user)
        
        # چک کن طرف مقابل پشتیبان هست
        from apps.assessments.models import ScientificGroupMembership
        is_support = ScientificGroupMembership.objects.filter(
            user=other_user,
            role="support_manager",
            is_active=True,
        ).exists()

        return render(request, self.template_name, {
            "conversation": conversation,
            "other_user": other_user,
            "is_support": is_support,
        })

    def post(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)
        text = request.POST.get("text", "")
        
        try:
            DirectMessageService.send_message(
                sender=request.user,
                receiver=other_user,
                text=text,
            )
        except ValueError as exc:
            messages.error(request, str(exc))
        
        # اگه طرف پشتیبان هست
        from apps.assessments.models import ScientificGroupMembership
        is_support = ScientificGroupMembership.objects.filter(
            user=other_user,
            role="support_manager",
            is_active=True,
        ).exists()

        if is_support:
            from apps.messaging.services.support_service import SupportService
            
            # چک FAQ
            faq_answer = SupportService.get_faq_answer(text)
            
            if faq_answer:
                DirectMessageService.send_message(
                    sender=other_user,
                    receiver=request.user,
                    text=faq_answer,
                )
            else:
                # پاسخ خودکار
                DirectMessageService.send_message(
                    sender=other_user,
                    receiver=request.user,
                    text="سلام! پیام شما دریافت شد. در اسرع وقت پاسخگو خواهیم بود.\n\n📞 برای پاسخگویی سریع‌تر، لطفاً نام و شماره تماس خود را ارسال کنید.",
                )
                
                # ارسال اطلاعات کاربر به پشتیبان
                user_info = (
                    f"📋 کاربر: {request.user.get_full_name() or request.user.username}\n"
                    f"ایمیل: {request.user.email or 'ندارد'}\n"
                    f"پیام: {text}"
                )
                DirectMessageService.send_message(
                    sender=request.user,
                    receiver=other_user,
                    text=user_info,
                )

        return redirect("messaging:direct-conversation", user_id=user_id)