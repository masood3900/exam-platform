from pathlib import Path

from django.core.exceptions import ValidationError


MAX_MESSAGE_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_MESSAGE_FILE_EXTENSIONS = {
    ".py",
    ".js",
    ".html",
    ".css",
    ".txt",
    ".pdf",
    ".docx",
    ".jpg",
    ".jpeg",
    ".png",
    ".zip",
}


def validate_message_file(value):

    if value is None:
        return

    if value.size > MAX_MESSAGE_FILE_SIZE:
        raise ValidationError(
            "حجم فایل نمی‌تواند بیشتر از ۱۰ مگابایت باشد."
        )

    extension = Path(value.name).suffix.lower()

    if extension not in ALLOWED_MESSAGE_FILE_EXTENSIONS:
        allowed = ", ".join(
            sorted(ALLOWED_MESSAGE_FILE_EXTENSIONS)
        )

        raise ValidationError(
            f"نوع فایل مجاز نیست. انواع مجاز: {allowed}"
        )
