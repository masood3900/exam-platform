from django.urls import reverse


class RoleService:

    @staticmethod
    def get_dashboard_url(user):

        # بالاترین سطح دسترسی
        if RoleService.is_staff(user):
            return reverse(
                "accounts:admin-dashboard"
            )


        # مدرس
        if RoleService.is_instructor(user):
            return reverse(
                "accounts:instructor-dashboard"
            )

        # دانش‌آموز
        if RoleService.is_student(user):
            return reverse(
                "accounts:dashboard"
            )

        # حالت پیش‌فرض
        return reverse(
            "accounts:dashboard"
        )

    @staticmethod
    def is_student(user):

        return user.groups.filter(
            name="Students"
        ).exists()

    @staticmethod
    def is_instructor(user):

        return user.groups.filter(
            name="Instructors"
        ).exists()

    @staticmethod
    def is_staff(user):

        return user.is_staff

    @staticmethod
    def is_superuser(user):

        return user.is_superuser

    @staticmethod
    def get_role(user):

        if user.is_superuser:
            return "superuser"

        if user.is_staff:
            return "staff"

        if RoleService.is_instructor(user):
            return "instructor"

        if RoleService.is_student(user):
            return "student"

        return "user"