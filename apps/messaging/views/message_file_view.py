from pathlib import Path

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404
from django.views import View

from apps.messaging.services.messaging_service import (
    MessagingService,
)


class MessageFileView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        message_id,
    ):

        message = MessagingService.get_message(
            message_id=message_id,
            user=request.user,
        )

        if not message.file:
            raise Http404(
                "فایلی برای این پیام وجود ندارد."
            )

        file_path = Path(
            message.file.path
        )

        if not file_path.exists():
            raise Http404(
                "فایل پیدا نشد."
            )

        return FileResponse(
            open(
                file_path,
                "rb",
            ),
            as_attachment=True,
            filename=file_path.name,
        )