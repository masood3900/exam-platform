import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image

from apps.assessments.models import QuestionImage


class ImageUploadService:
    """سرویس آپلود و بهینه‌سازی عکس"""

    MAX_SIZE_MB = 3
    MAX_DIMENSION = 1600
    ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]

    @staticmethod
    def validate(file):
        """اعتبارسنجی فایل"""
        # چک حجم
        if file.size > ImageUploadService.MAX_SIZE_MB * 1024 * 1024:
            raise ValueError(f"حجم فایل بیش از {ImageUploadService.MAX_SIZE_MB} مگابایت است.")

        # چک پسوند
        ext = file.name.split('.')[-1].lower()
        if ext not in ImageUploadService.ALLOWED_EXTENSIONS:
            raise ValueError(f"فرمت مجاز: {', '.join(ImageUploadService.ALLOWED_EXTENSIONS)}")

        # چک تصویر بودن
        try:
            img = Image.open(file)
            img.verify()
            file.seek(0)
        except Exception:
            raise ValueError("فایل انتخابی یک تصویر معتبر نیست.")

        return True

    @staticmethod
    def optimize(file):
        """Resize و تبدیل به WebP"""
        img = Image.open(file)

        # تبدیل RGBA به RGB برای WebP
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        # Resize اگه بزرگ‌تر از حد مجاز
        if img.width > ImageUploadService.MAX_DIMENSION or img.height > ImageUploadService.MAX_DIMENSION:
            img.thumbnail(
                (ImageUploadService.MAX_DIMENSION, ImageUploadService.MAX_DIMENSION),
                Image.LANCZOS,
            )

        # ذخیره به WebP
        output = BytesIO()
        img.save(output, format="WEBP", quality=85, optimize=True)
        output.seek(0)

        return output

    @staticmethod
    def upload(file, user):
        """آپلود فایل"""
        ImageUploadService.validate(file)

        original_name = file.name

        # بهینه‌سازی
        optimized = ImageUploadService.optimize(file)

        # نام جدید
        base_name = os.path.splitext(original_name)[0][:50]
        new_name = f"{base_name}.webp"

        # ساخت QuestionImage
        question_image = QuestionImage(
            uploaded_by=user,
            original_name=original_name,
            file_size=optimized.getbuffer().nbytes,
        )
        question_image.image.save(new_name, ContentFile(optimized.read()), save=True)

        return question_image
