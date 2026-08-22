from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from apps.accounts.services.role_service import RoleService


class InstructorRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):

        if not RoleService.is_instructor(request.user):
            raise PermissionDenied

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )


class AdminRequiredMixin(LoginRequiredMixin):

    def dispatch(
        self,
        request,
        *args,
        **kwargs,
    ):

        if not RoleService.is_staff(request.user):
            raise PermissionDenied

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )