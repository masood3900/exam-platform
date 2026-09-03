from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError

from apps.assessments.models import Assessment, Attempt


class AssessmentDeleteView(LoginRequiredMixin, View):
    """حذف آزمون"""

    def post(self, request, assessment_id):
        assessment = get_object_or_404(
            Assessment.objects.select_related(
                "course",
                "learning_path",
                "scientific_group",
            ),
            id=assessment_id,
        )

        title = assessment.title

        # بررسی تلاش‌های ثبت شده برای این آزمون
        attempts = Attempt.objects.filter(
            assessment=assessment,
        ).select_related("student")

        if attempts.exists():
            # جمع‌آوری اطلاعات دانشجوها
            students = []
            for attempt in attempts:
                student_name = (
                    attempt.student.get_full_name()
                    or attempt.student.username
                )
                if student_name not in students:
                    students.append(student_name)

            students_count = len(students)
            attempts_count = attempts.count()

            # نمایش پیام راهنما
            student_list = "، ".join(students[:10])
            if students_count > 10:
                student_list += f" و {students_count - 10} نفر دیگر"

            messages.warning(
                request,
                f"آزمون «{title}» قابل حذف نیست، زیرا "
                f"{students_count} دانشجو ({attempts_count} تلاش) "
                f"از این آزمون استفاده کرده‌اند.\n"
                f"دانشجویان: {student_list}"
            )
        else:
            try:
                assessment.delete()
                messages.success(
                    request,
                    f"آزمون «{title}» حذف شد.",
                )
            except ProtectedError as e:
                messages.error(
                    request,
                    f"آزمون «{title}» به دلیل استفاده در بخش‌های دیگر "
                    f"قابل حذف نیست. لطفاً ابتدا موارد وابسته را حذف کنید.",
                )

        return redirect("accounts:scientific_manager:dashboard")
