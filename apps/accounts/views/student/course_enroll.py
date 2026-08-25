from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.assessments.models import Course
from apps.assessments.services.enrollment_service import (
    EnrollmentService,
)


class CourseEnrollView(
    LoginRequiredMixin,
    View,
):

    def post(
        self,
        request,
        pk,
    ):

        course = get_object_or_404(
            Course,
            pk=pk,
            is_active=True,
        )

        try:
            enrollment = (
                EnrollmentService.enroll(
                    user=request.user,
                    course=course,
                )
            )

        except ValueError as exc:
            messages.error(
                request,
                str(exc),
            )

            return redirect(
                "accounts:dashboard"
            )

        except IntegrityError:
            messages.error(
                request,
                "ثبت‌نام انجام نشد. لطفاً دوباره تلاش کنید.",
            )

            return redirect(
                "accounts:dashboard"
            )

        if enrollment.has_access:
            messages.success(
                request,
                f"دوره «{course.name}» با موفقیت به داشبورد شما اضافه شد.",
            )
        else:
            messages.info(
                request,
                f"دوره «{course.name}» ثبت شد و پس از پرداخت فعال خواهد شد.",
            )

        return redirect(
            "accounts:dashboard"
        )