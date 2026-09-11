from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView

from apps.assessments.models import (
    Course,
    CourseEnrollment,
    Assessment,
    ScientificGroup,
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

        context["categories"] = ScientificGroup.objects.filter(
            parent__isnull=True,
            is_active=True,
        ).exclude(
            name__icontains="فنی"
        ).prefetch_related("children")

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
        ).order_by("-created_at")


class CourseDetailPublicView(DetailView):
    """جزئیات دوره"""

    model = Course
    template_name = "core/course_detail.html"
    context_object_name = "course"


class AssessmentListView(ListView):
    """لیست آزمون‌ها - قابل فیلتر بر اساس حوزه یا مسیر"""

    model = Assessment
    template_name = "core/assessment_list.html"
    context_object_name = "assessments"
    paginate_by = 12

    def get_queryset(self):
        queryset = Assessment.objects.filter(
            is_active=True,
            course__isnull=True,
        ).order_by("-created_at")

        # فیلتر بر اساس حوزه یا مسیر
        category_id = self.request.GET.get("category")
        if category_id:
            # گروه انتخاب شده
            try:
                group = ScientificGroup.objects.get(id=category_id)
                
                # اگه رشته (parent) باشه، همه مسیرها و موضوع‌های زیرش
                if group.parent is None:
                    # جمع‌آوری همه زیرمجموعه‌ها
                    descendants = []
                    children = ScientificGroup.objects.filter(parent=group)
                    for child in children:
                        descendants.append(child.id)
                        # زیرمجموعه‌های عمیق‌تر
                        grandchildren = ScientificGroup.objects.filter(parent=child)
                        for gc in grandchildren:
                            descendants.append(gc.id)
                    
                    queryset = queryset.filter(scientific_group_id__in=descendants)
                
                # اگه مسیر باشه، خودش و موضوع‌های زیرش
                elif group.parent.parent is None:
                    descendants = [group.id]
                    children = ScientificGroup.objects.filter(parent=group)
                    for child in children:
                        descendants.append(child.id)
                    
                    queryset = queryset.filter(scientific_group_id__in=descendants)
                
                # اگه موضوع باشه، فقط خودش
                else:
                    queryset = queryset.filter(scientific_group=group)
                    
            except ScientificGroup.DoesNotExist:
                pass

        return queryset

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

        # اطلاعات گروه انتخاب شده
        category_id = self.request.GET.get("category")
        if category_id:
            try:
                context["selected_category"] = ScientificGroup.objects.get(id=category_id)
            except ScientificGroup.DoesNotExist:
                context["selected_category"] = None

        return context


class AssessmentDetailView(DetailView):
    """جزئیات آزمون"""

    model = Assessment
    template_name = "core/assessment_detail.html"
    context_object_name = "assessment"
    pk_url_kwarg = "assessment_id"

    def get_context_data(self, **kwargs):
        from apps.assessments.models import (
            AssessmentEnrollment,
            PaymentRequest,
            Attempt,
        )

        context = super().get_context_data(**kwargs)
        assessment = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            context["user_has_access"] = AssessmentAccessService.can_user_access(
                user,
                assessment,
            )

            # Enrollment
            enrollment = AssessmentEnrollment.objects.filter(
                user=user,
                assessment=assessment,
            ).first()
            context["enrollment"] = enrollment

            # آیا قبلاً پرداخت شده؟
            has_paid_before = AssessmentEnrollment.objects.filter(
                user=user,
                assessment=assessment,
                payment_status=AssessmentEnrollment.PaymentStatus.PAID,
            ).exists()
            context["has_paid_before"] = has_paid_before

            # تعداد تلاش‌های استفاده شده
            used_attempts = Attempt.objects.filter(
                student=user,
                assessment=assessment,
            ).exclude(
                status__in=[
                    Attempt.Status.CREATED,
                    Attempt.Status.CANCELLED,
                ],
            ).count()
            context["used_attempts"] = used_attempts

            # آیا درخواست پرداخت در انتظار داره؟
            has_payment_request = PaymentRequest.objects.filter(
                user=user,
                assessment=assessment,
                status=PaymentRequest.Status.PENDING,
            ).exists()
            context["has_payment_request"] = has_payment_request

        return context
