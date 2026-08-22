from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.messaging.services.messaging_service import (
    MessagingService,
)


class ConversationInboxView(
    LoginRequiredMixin,
    View,
):

    template_name = (
        "messaging/inbox.html"
    )

    def get(
        self,
        request,
    ):

        conversations = (
            MessagingService.get_inbox(
                request.user,
            )
        )

        return render(
            request,
            self.template_name,
            {
                "conversations": conversations,
            },
        )

    def post(
        self,
        request,
    ):

        conversation_id = request.POST.get(
            "conversation_id",
        )

        conversation = (
            MessagingService.get_conversation(
                conversation_id,
                request.user,
            )
        )

        MessagingService.hide_conversation(
            conversation,
            request.user,
        )

        return redirect(
            "messaging:inbox",
        )
