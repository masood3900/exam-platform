from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from apps.accounts.services.role_service import RoleService


class InstructorRequiredMixin(LoginRequiredMixin):
    """میکسین برای مدرس"""

    def dispatch(self, request, *args, **kwargs):
        if not RoleService.is_instructor(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(LoginRequiredMixin):
    """میکسین برای ادمین"""

    def dispatch(self, request, *args, **kwargs):
        if not RoleService.is_staff(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AdminOrScientificManagerRequiredMixin(LoginRequiredMixin):
    """میکسین برای ادمین یا مدیر علمی"""

    def dispatch(self, request, *args, **kwargs):
        if not (
            RoleService.is_staff(request.user) or
            RoleService.is_scientific_manager(request.user)
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class StaffOrInstructorRequiredMixin(LoginRequiredMixin):
    """میکسین برای ادمین، مدیر علمی، مدرس"""

    def dispatch(self, request, *args, **kwargs):
        if not (
            RoleService.is_staff(request.user) or
            RoleService.is_scientific_manager(request.user) or
            RoleService.is_instructor(request.user)
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)