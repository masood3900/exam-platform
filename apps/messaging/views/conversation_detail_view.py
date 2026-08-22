
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.messaging.services.messaging_service import (
    MessagingService,
)


class ConversationDetailView(
    LoginRequiredMixin,
    View,
):

    template_name = (
        "messaging/conversation_detail.html"
    )

    def get(
        self,
        request,
        conversation_id,
    ):

        conversation = (
            MessagingService.get_conversation(
                conversation_id,
                request.user,
            )
        )

        conversation_messages = (
            MessagingService.get_messages(
                conversation,
                request.user,
            )
        )

        return render(
            request,
            self.template_name,
            {
                "conversation": conversation,
                "conversation_messages": conversation_messages,
            },
        )

    def post(
        self,
        request,
        conversation_id,
    ):

        conversation = (
            MessagingService.get_conversation(
                conversation_id,
                request.user,
            )
        )

        text = request.POST.get(
            "text",
            "",
        )

        file = request.FILES.get(
            "file",
        )

        try:

            MessagingService.send_message(
                conversation=conversation,
                sender=request.user,
                text=text,
                file=file,
            )

        except ValueError as exc:

            conversation_messages = (
                MessagingService.get_messages(
                    conversation,
                    request.user,
                )
            )

            return render(
                request,
                self.template_name,
                {
                    "conversation": conversation,
                    "conversation_messages": conversation_messages,
                    "error": str(exc),
                },
            )

        return redirect(
            "messaging:conversation-detail",
            conversation_id=conversation.id,
        )

