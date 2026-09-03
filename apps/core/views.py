from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView

from apps.assessments.models import (
    Course,
    CourseEnrollment,
    Assessment,
)
from apps.accounts.services.role_service import RoleService
from apps.assessments.services.assessment_access_service import (
    AssessmentAccessService,
)


class HomeView(TemplateView):
    """صفحه اصلی - برای همه"""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        courses = Course.objects.filter(
            is_active=True,
            parent__isnull=False,
        ).select_related("learning_path", "parent")

        context["courses"] = courses

        # آزمون‌های ویژه
        context["featured_assessments"] = Assessment.objects.filter(
            is_active=True,
            is_public=True,
        )[:6]

        return context


class CourseListView(ListView):
    """لیست همه دوره‌ها"""

    model = Course
    template_name = "core/course_list.html"
    context_object_name = "courses"
    paginate_by = 12

    def get_queryset(self):
        return Course.objects.filter(
            is_active=True,
            parent__isnull=False,
        ).select_related(
            "learning_path",
            "parent",
        ).prefetch_related(
            "course_instructor_assignments",
            "course_instructor_assignments__instructor",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = context["courses"]

        if self.request.user.is_authenticated:
            user_enrollments = CourseEnrollment.objects.filter(
                user=self.request.user,
                course__in=courses,
            )
            enrollment_map = {
                enrollment.course_id: enrollment
                for enrollment in user_enrollments
            }

            for course in courses:
                course.user_enrollment = enrollment_map.get(course.id)

        return context


class CourseDetailPublicView(DetailView):
    """صفحه عمومی دوره"""

    model = Course
    template_name = "core/course_detail.html"
    context_object_name = "course"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        return Course.objects.filter(
            is_active=True,
            parent__isnull=False,
        ).select_related(
            "learning_path",
            "parent",
            "scientific_group",
        ).prefetch_related(
            "categories",
            "course_instructor_assignments",
            "course_instructor_assignments__instructor",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        if self.request.user.is_authenticated:
            enrollment = CourseEnrollment.objects.filter(
                user=self.request.user,
                course=course,
            ).first()
            context["enrollment"] = enrollment

        return context


class AssessmentListView(ListView):
    """لیست همه آزمون‌های مستقل"""

    model = Assessment
    template_name = "core/assessment_list.html"
    context_object_name = "assessments"
    paginate_by = 12

    def get_queryset(self):
        return Assessment.objects.filter(
            is_active=True,
            course__isnull=True,
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assessments = context["assessments"]

        if self.request.user.is_authenticated:
            for assessment in assessments:
                assessment.user_has_access = (
                    AssessmentAccessService.can_user_access(
                        self.request.user,
                        assessment,
                    )
                )

        return context


class AssessmentDetailView(DetailView):
    """صفحه جزئیات آزمون"""

    model = Assessment
    template_name = "core/assessment_detail.html"
    context_object_name = "assessment"
    pk_url_kwarg = "assessment_id"

    def get_queryset(self):
        return Assessment.objects.filter(is_active=True).select_related(
            "scientific_group",
            "course",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assessment = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            from apps.assessments.models import AssessmentEnrollment, PaymentRequest

            context["used_attempts"] = AssessmentAccessService.used_attempts(
                user,
                assessment,
            )

            enrollment = AssessmentEnrollment.objects.filter(
                user=user,
                assessment=assessment,
            ).first()
            context["enrollment"] = enrollment

            context["has_payment_request"] = PaymentRequest.objects.filter(
                user=user,
                assessment=assessment,
                status=PaymentRequest.Status.PENDING,
            ).exists()

            context["has_paid_before"] = PaymentRequest.objects.filter(
                user=user,
                assessment=assessment,
                status=PaymentRequest.Status.APPROVED,
            ).exists()

        return context