from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.assessments.models import Course, CourseEnrollment


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
            with transaction.atomic():

                enrollment, created = (
                    CourseEnrollment.objects.get_or_create(
                        user=request.user,
                        course=course,
                    )
                )

                if not created:
                    if enrollment.has_access:
                        messages.info(
                            request,
                            "شما قبلاً به این دوره دسترسی دارید.",
                        )
                    else:
                        messages.info(
                            request,
                            "ثبت‌نام شما برای این دوره قبلاً انجام شده است.",
                        )

                    return redirect(
                        "accounts:dashboard"
                    )

                if course.is_free:
                    enrollment.status = (
                        CourseEnrollment.Status.ACTIVE
                    )
                    enrollment.payment_status = (
                        CourseEnrollment.PaymentStatus.NOT_REQUIRED
                    )
                else:
                    enrollment.status = (
                        CourseEnrollment.Status.PENDING
                    )
                    enrollment.payment_status = (
                        CourseEnrollment.PaymentStatus.UNPAID
                    )

                enrollment.save(
                    update_fields=[
                        "status",
                        "payment_status",
                    ]
                )

        except IntegrityError:
            messages.error(
                request,
                "ثبت‌نام انجام نشد. لطفاً دوباره تلاش کنید.",
            )

            return redirect(
                "accounts:dashboard"
            )

        if course.is_free:
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