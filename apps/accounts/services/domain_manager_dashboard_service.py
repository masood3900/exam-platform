from django.db.models import Count, Avg

from apps.assessments.models import (
    ScientificGroup,
    ScientificGroupMembership,
    Course,
    Assessment,
)


class DomainManagerDashboardService:
    """سرویس داشبورد مدیر کل"""

    @staticmethod
    def get_domains(user):
        """حوزه‌هایی که کاربر مدیر کلشونه"""
        return ScientificGroup.objects.filter(
            memberships__user=user,
            memberships__role="domain_manager",
            memberships__is_active=True,
            is_active=True,
        ).distinct()

    @staticmethod
    def overall_stats(user):
        """آمار کلی حوزه"""
        domains = DomainManagerDashboardService.get_domains(user)

        fields = ScientificGroup.objects.filter(
            parent__in=domains,
            is_active=True,
        )

        topics = ScientificGroup.objects.filter(parent__in=fields)
        all_groups = list(fields) + list(topics)

        courses = Course.objects.filter(
            scientific_group__in=all_groups,
            is_active=True,
        )

        assessments = Assessment.objects.filter(
            scientific_group__in=all_groups,
            is_active=True,
        )

        return {
            "domains_count": domains.count(),
            "fields_count": fields.count(),
            "courses_count": courses.count(),
            "assessments_count": assessments.count(),
        }

    @staticmethod
    def get_fields(user):
        """رشته‌های حوزه"""
        domains = DomainManagerDashboardService.get_domains(user)
        return ScientificGroup.objects.filter(
            parent__in=domains,
            is_active=True,
        )

    @staticmethod
    def get_courses(user):
        """دوره‌های حوزه"""
        domains = DomainManagerDashboardService.get_domains(user)
        fields = ScientificGroup.objects.filter(parent__in=domains)
        topics = ScientificGroup.objects.filter(parent__in=fields)
        all_groups = list(fields) + list(topics)
        return Course.objects.filter(
            scientific_group__in=all_groups,
            is_active=True,
        ).select_related("scientific_group")

    @staticmethod
    def get_assessments(user):
        """آزمون‌های حوزه"""
        domains = DomainManagerDashboardService.get_domains(user)
        fields = ScientificGroup.objects.filter(parent__in=domains)
        topics = ScientificGroup.objects.filter(parent__in=fields)
        all_groups = list(fields) + list(topics)
        return Assessment.objects.filter(
            scientific_group__in=all_groups,
            is_active=True,
        ).select_related("scientific_group")


    @staticmethod
    def get_managers(user):
        """مدیران علمی حوزه"""
        domains = DomainManagerDashboardService.get_domains(user)
        return ScientificGroupMembership.objects.filter(
            scientific_group__parent__in=domains,
            role="scientific_manager",
            is_active=True,
        ).select_related("user", "scientific_group")
