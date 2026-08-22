from apps.messaging.services.messaging_service import (
    MessagingService,
)


def messaging_context(request):

    if not request.user.is_authenticated:

        return {
            "unread_message_count": 0,
        }

    return {
        "unread_message_count":
            MessagingService.get_unread_message_count(
                request.user,
            ),
    }