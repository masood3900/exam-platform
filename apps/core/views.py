from django.views.generic import TemplateView

from apps.assessments.models import (
    Course,
    CourseEnrollment,
)


class HomeView(TemplateView):

    template_name = "core/home.html"

    def get_context_data(
        self,
        **kwargs,
    ):

        context = super().get_context_data(
            **kwargs
        )

        # فقط دوره‌های واقعی را نمایش می‌دهیم.
        # Courseهای بدون parent نقش موضوع/حوزه دارند.
        courses = list(
            Course.objects
            .filter(
                is_active=True,
                parent__isnull=False,
            )
            .select_related(
                "learning_path",
                "parent",
            )
        )

        enrollment_map = {}

        if self.request.user.is_authenticated:

            enrollments = (
                CourseEnrollment.objects
                .filter(
                    user=self.request.user,
                    course__in=courses,
                )
                .select_related(
                    "course",
                )
            )

            enrollment_map = {
                enrollment.course_id: enrollment
                for enrollment in enrollments
            }

        course_items = [
            {
                "course": course,
                "enrollment": enrollment_map.get(
                    course.id
                ),
            }
            for course in courses
        ]

        context["course_items"] = course_items

        return context