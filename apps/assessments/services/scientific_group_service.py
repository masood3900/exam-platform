from apps.assessments.models import (
    ScientificGroup,
    ScientificGroupMembership,
)


class ScientificGroupService:

    @staticmethod
    def is_member(
        user,
        group,
    ):
        return ScientificGroupMembership.objects.filter(
            user=user,
            scientific_group=group,
            is_active=True,
        ).exists()

    @staticmethod
    def has_role(
        user,
        group,
        role,
    ):
        return ScientificGroupMembership.objects.filter(
            user=user,
            scientific_group=group,
            role=role,
            is_active=True,
        ).exists()

    @staticmethod
    def get_membership(
        user,
        group,
    ):
        return (
            ScientificGroupMembership.objects
            .filter(
                user=user,
                scientific_group=group,
                is_active=True,
            )
            .first()
        )

    @staticmethod
    def get_user_groups(
        user,
    ):
        return (
            ScientificGroup.objects
            .filter(
                memberships__user=user,
                memberships__is_active=True,
                is_active=True,
            )
            .distinct()
        )

    @staticmethod
    def is_scientific_manager(
        user,
        group,
    ):
        return ScientificGroupService.has_role(
            user=user,
            group=group,
            role=(
                ScientificGroupMembership.Role
                .SCIENTIFIC_MANAGER
            ),
        )

    @staticmethod
    def is_question_designer(
        user,
        group,
    ):
        return ScientificGroupService.has_role(
            user=user,
            group=group,
            role=(
                ScientificGroupMembership.Role
                .QUESTION_DESIGNER
            ),
        )

    @staticmethod
    def is_instructor(
        user,
        group,
    ):
        return ScientificGroupService.has_role(
            user=user,
            group=group,
            role=(
                ScientificGroupMembership.Role
                .INSTRUCTOR
            ),
        )
