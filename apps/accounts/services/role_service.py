from django.urls import reverse


class RoleService:
    """سرویس مدیریت نقش‌ها و دسترسی‌ها"""

    # اولویت نقش‌ها از بالا به پایین
    ROLE_PRIORITY = {
        'superuser': 5,
        'staff': 4,
        'scientific_manager': 3,
        'instructor': 2,
        'question_designer': 2,
        'student': 1,
        'user': 0,
    }

    @staticmethod
    def get_dashboard_url(user):
        """دریافت آدرس داشبورد بر اساس بالاترین نقش کاربر"""
        
        role = RoleService.get_role(user)
        
        dashboard_urls = {
            "superuser": "accounts:admin-dashboard",
            "staff": "accounts:admin-dashboard",
            "domain_manager": "accounts:domain_manager:dashboard",
            "support_manager": "accounts:support_manager:dashboard",
            "technical_manager": "accounts:admin-dashboard",  # فعلاً ادمین
            "financial_manager": "accounts:financial_manager:dashboard",
            "scientific_manager": "accounts:scientific_manager:dashboard",
            "question_designer": "accounts:question_designer:dashboard",
            "student": "accounts:dashboard",
            "user": "core:home",
        }
        
        url_name = dashboard_urls.get(role, "accounts:dashboard")
        return reverse(url_name)

    @staticmethod
    def get_available_dashboards(user):
        """دریافت لیست داشبوردهای در دسترس کاربر"""
        
        dashboards = []
        
        if not user.is_authenticated:
            return dashboards
        
        # داشبورد ادمین
        if user.is_staff or user.is_superuser:
            dashboards.append({
                "name": "داشبورد مدیریت",
                "url": reverse("accounts:admin-dashboard"),
                "icon": "📊",
            })
        # داشبورد مدیر کل
        if RoleService.is_domain_manager(user):
            dashboards.append({
                "name": "داشبورد مدیر کل",
                "url": reverse("accounts:domain_manager:dashboard"),
                "icon": "🏛️",
            })
        # داشبورد مدیر مالی
        if RoleService.is_financial_manager(user):
            dashboards.append({
                "name": "داشبورد مدیر مالی",
                "url": reverse("accounts:financial_manager:dashboard"),
                "icon": "💰",
            })
        
        
        # داشبورد مدیر پشتیبانی
        if RoleService.is_support_manager(user):
            dashboards.append({
                "name": "داشبورد پشتیبانی",
                "url": reverse("accounts:support_manager:dashboard"),
                "icon": "🎧",
            })

        # داشبورد مدیر علمی
        if RoleService.is_scientific_manager(user):
            dashboards.append({
                "name": "داشبورد مدیر علمی",
                "url": reverse("accounts:scientific_manager:dashboard"),
                "icon": "🔬",
            })
        # داشبورد طراح سوال
        if RoleService.is_question_designer(user):
            dashboards.append({
                "name": "داشبورد طراح سوال",
                "url": reverse("accounts:question_designer:dashboard"),
                "icon": "✏️",
            })
        
        # داشبورد مدرس - غیرفعال
        # if RoleService.is_instructor(user):
        #     dashboards.append({
        #         "name": "داشبورد مدرس",
        #         "url": reverse("accounts:instructor-dashboard"),
        #         "icon": "👨‍🏫",
        #     })
        
        # داشبورد دانش‌آموز
        if RoleService.is_student(user):
            dashboards.append({
                "name": "داشبورد دانشجو",
                "url": reverse("accounts:dashboard"),
                "icon": "👨‍🎓",
            })
        
        return dashboards
    

    @staticmethod
    def is_student(user):
        """بررسی نقش دانش‌آموز"""
        if not user.is_authenticated:
            return False
        if user.groups.filter(name="Students").exists():
            return True
        from apps.assessments.models import AssessmentEnrollment
        return AssessmentEnrollment.objects.filter(
            user=user,
            status="active",
        ).exists()

    @staticmethod
    def is_instructor(user):
        """بررسی نقش مدرس"""
        if not user.is_authenticated:
            return False
        return user.groups.filter(name="Instructors").exists()

    @staticmethod
    def is_staff(user):
        """بررسی نقش مدیر"""
        return user.is_authenticated and user.is_staff

    @staticmethod
    def is_superuser(user):
        """بررسی نقش سوپریوزر"""
        return user.is_authenticated and user.is_superuser

    @staticmethod
    def is_scientific_manager(user):
        """بررسی نقش مدیر علمی"""
        if not user.is_authenticated:
            return False
        
        from apps.assessments.models import ScientificGroupMembership
        
        return ScientificGroupMembership.objects.filter(
            user=user,
            role=ScientificGroupMembership.Role.SCIENTIFIC_MANAGER,
            is_active=True,
        ).exists()

    @staticmethod
    def is_question_designer(user):
        """بررسی نقش طراح سوال"""
        if not user.is_authenticated:
            return False
        
        from apps.assessments.models import ScientificGroupMembership
        
        return ScientificGroupMembership.objects.filter(
            user=user,
            role=ScientificGroupMembership.Role.QUESTION_DESIGNER,
            is_active=True,
        ).exists()
    @staticmethod
    def is_technical_manager(user):
        """بررسی نقش مدیر کل فنی"""
        if not user.is_authenticated:
            return False
        from apps.assessments.models import ScientificGroupMembership
        return ScientificGroupMembership.objects.filter(
            user=user,
            role=ScientificGroupMembership.Role.TECHNICAL_MANAGER,
            is_active=True,
        ).exists()

    @staticmethod
    def is_financial_manager(user):
        """بررسی نقش مدیر مالی"""
        if not user.is_authenticated:
            return False
        from apps.assessments.models import ScientificGroupMembership
        return ScientificGroupMembership.objects.filter(
            user=user,
            role=ScientificGroupMembership.Role.FINANCIAL_MANAGER,
            is_active=True,
        ).exists()

    @staticmethod
    def is_support_manager(user):
        """بررسی نقش مدیر پشتیبانی"""
        if not user.is_authenticated:
            return False
        from apps.assessments.models import ScientificGroupMembership
        return ScientificGroupMembership.objects.filter(
            user=user,
            role="support_manager",
            is_active=True,
        ).exists()

    @staticmethod
    def is_domain_manager(user):
        """بررسی نقش مدیر کل"""
        if not user.is_authenticated:
            return False
        
        from apps.assessments.models import ScientificGroupMembership
        
        return ScientificGroupMembership.objects.filter(
            user=user,
            role=ScientificGroupMembership.Role.DOMAIN_MANAGER,
            is_active=True,
        ).exists()

    @staticmethod
    def get_role(user):
        if not user.is_authenticated:
            return "anonymous"

        if not user.is_authenticated:
            return "anonymous"
    
        if user.is_superuser:
            return "superuser"
    
        if user.is_staff:
            return "staff"
    
        if RoleService.is_domain_manager(user):
            return "domain_manager"
    
        if RoleService.is_technical_manager(user):
            return "technical_manager"
    
        if RoleService.is_financial_manager(user):
            return "financial_manager"
        if RoleService.is_support_manager(user):
            return "support_manager"

    
        if RoleService.is_scientific_manager(user):
            return "scientific_manager"
    
        # if RoleService.is_instructor(user):
        #     return "instructor"
    
        if RoleService.is_question_designer(user):
            return "question_designer"
    
        if RoleService.is_student(user):
            return "student"
    
        from apps.assessments.models import AssessmentEnrollment
        if AssessmentEnrollment.objects.filter(
            user=user,
            status="active",
        ).exists():
            return "student"

        return "user"
    
    @staticmethod
    def get_all_roles(user):
        """دریافت همه نقش‌های کاربر"""
        
        roles = []
        
        if not user.is_authenticated:
            return roles
        
        if user.is_superuser:
            roles.append("superuser")
        
        if user.is_staff:
            roles.append("staff")
        
        if RoleService.is_scientific_manager(user):
            roles.append("scientific_manager")
        
        if RoleService.is_instructor(user):
            roles.append("instructor")
        
        if RoleService.is_question_designer(user):
            roles.append("question_designer")
        
        if RoleService.is_student(user):
            roles.append("student")
        
        if not roles:
            roles.append("user")
        
        return roles

    