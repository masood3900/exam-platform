from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.assessments.services.image_upload_service import ImageUploadService


class ImageUploadView(LoginRequiredMixin, View):
    """آپلود عکس برای سوالات توسط طراح سوال"""

    def post(self, request):
        # چک نقش
        from apps.accounts.services.role_service import RoleService
        if not RoleService.is_question_designer(request.user):
            return JsonResponse(
                {"error": "شما اجازه آپلود عکس ندارید."},
                status=403,
            )

        file = request.FILES.get("image")

        if not file:
            return JsonResponse(
                {"error": "فایلی انتخاب نشده است."},
                status=400,
            )

        try:
            question_image = ImageUploadService.upload(file, request.user)

            # URL مطلق
            url = question_image.image.url
            if not url.startswith('http'):
                url = request.build_absolute_uri(url)

            return JsonResponse({
                "success": True,
                "url": url,
                "id": str(question_image.id),
                "size": question_image.file_size,
            })

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": f"خطا در آپلود: {str(e)}"},
                status=500,
            )
