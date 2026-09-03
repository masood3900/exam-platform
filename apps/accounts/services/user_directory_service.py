from django.contrib.auth import get_user_model

User = get_user_model()


class UserDirectoryService:
    """سرویس جامع مدیریت و نمایش کاربران"""

    @staticmethod
    def get_users_by_role(role, scope_user=None):
        """کاربران بر اساس نقش"""
        from apps.assessments.models import ScientificGroupMembership, CourseEnrollment

        if role == "domain_manager":
            return User.objects.filter(
                scientific_group_memberships__role="domain_manager",
                scientific_group_memberships__is_active=True,
            ).distinct()

        elif role == "scientific_manager":
            return User.objects.filter(
                scientific_group_memberships__role="scientific_manager",
                scientific_group_memberships__is_active=True,
            ).distinct()

        elif role == "question_designer":
            return User.objects.filter(
                scientific_group_memberships__role="question_designer",
                scientific_group_memberships__is_active=True,
            ).distinct()

        elif role == "student":
            from apps.assessments.models import AssessmentEnrollment
            return User.objects.filter(
                assessment_enrollments__status="active",
            ).distinct()

        elif role == "guest":
            return User.objects.exclude(
                scientific_group_memberships__is_active=True,
            ).exclude(
                course_enrollments__status="active",
            ).exclude(is_staff=True)

        return User.objects.none()

    @staticmethod
    def get_scoped_users_by_role(role, scope_user):
        """کاربران با محدوده دسترسی مدیر"""
        from apps.assessments.models import ScientificGroupMembership

        managed_groups = list(ScientificGroupMembership.objects.filter(
            user=scope_user,
            is_active=True,
        ).values_list("scientific_group_id", flat=True))

        # شامل فرزندها
        from apps.assessments.models import ScientificGroup
        all_ids = list(managed_groups)
        for gid in managed_groups:
            children = ScientificGroup.objects.filter(parent_id=gid).values_list('id', flat=True)
            all_ids.extend(children)
        managed_groups = all_ids

        if role == "domain_manager":
            return User.objects.filter(
                scientific_group_memberships__scientific_group_id__in=managed_groups,
                scientific_group_memberships__role="domain_manager",
                scientific_group_memberships__is_active=True,
            ).distinct()

        elif role == "scientific_manager":
            return User.objects.filter(
                scientific_group_memberships__scientific_group_id__in=managed_groups,
                scientific_group_memberships__role="scientific_manager",
                scientific_group_memberships__is_active=True,
            ).distinct()

        elif role == "question_designer":
            return User.objects.filter(
                scientific_group_memberships__scientific_group_id__in=managed_groups,
                scientific_group_memberships__role="question_designer",
                scientific_group_memberships__is_active=True,
            ).distinct()

        elif role == "student":
            from apps.assessments.models import AssessmentEnrollment, Assessment
            managed_assessments = Assessment.objects.filter(
                scientific_group_id__in=managed_groups,
            )
            return User.objects.filter(
                assessment_enrollments__assessment__in=managed_assessments,
                assessment_enrollments__status="active",
            ).distinct()

        elif role == "guest":
            return User.objects.exclude(
                scientific_group_memberships__is_active=True,
            ).exclude(
                course_enrollments__status="active",
            ).exclude(is_staff=True)

        return User.objects.none()

    @staticmethod
    def get_user_card_data(user, role_label=None, role_color="primary"):
        """داده‌های کارت کاربر"""
        avatar = None
        age = None

        if hasattr(user, 'profile'):
            profile = user.profile
            if profile.avatar:
                avatar = profile.avatar.url
            if profile.birth_date:
                from django.utils import timezone
                today = timezone.now().date()
                age = today.year - profile.birth_date.year - (
                    (today.month, today.day) < (profile.birth_date.month, profile.birth_date.day)
                )

        # پیدا کردن گروه
        group_name = None
        from apps.assessments.models import ScientificGroupMembership
        membership = ScientificGroupMembership.objects.filter(
            user=user,
            is_active=True,
        ).select_related("scientific_group").first()
        if membership:
            group_name = membership.scientific_group.name

        return {
            "user": user,
            "full_name": user.get_full_name() or user.username,
            "avatar": avatar,
            "age": age,
            "date_joined": user.date_joined,
            "role_label": role_label or "کاربر",
            "role_color": role_color,
            "group_name": group_name,
        }

    @staticmethod
    def get_directory_data(scope_user=None, exclude_roles=None):
        """همه گروه‌های کاربران با داده کارت"""

        role_configs = {
            "domain_managers": {
                "title": "مدیران کل",
                "color": "primary",
                "label": "مدیر کل",
                "role": "domain_manager",
            },
            "scientific_managers": {
                "title": "مدیران علمی",
                "color": "info",
                "label": "مدیر علمی",
                "role": "scientific_manager",
            },
            "question_designers": {
                "title": "طراحان سوال",
                "color": "warning",
                "label": "طراح سوال",
                "role": "question_designer",
            },
            "students": {
                "title": "دانشجویان",
                "color": "success",
                "label": "دانشجو",
                "role": "student",
            },
            "guests": {
                "title": "مهمان‌ها",
                "color": "secondary",
                "label": "مهمان",
                "role": "guest",
            },
        }

        if exclude_roles:
            for role_key in exclude_roles:
                role_configs.pop(role_key, None)

        directory = {}
        for key, config in role_configs.items():
            if scope_user:
                users = UserDirectoryService.get_scoped_users_by_role(
                    config["role"], scope_user
                )
            else:
                users = UserDirectoryService.get_users_by_role(config["role"])

            card_data_list = []
            for user in users:
                card_data_list.append(
                    UserDirectoryService.get_user_card_data(
                        user,
                        role_label=config["label"],
                        role_color=config["color"],
                    )
                )

            directory[key] = {
                "title": config["title"],
                "color": config["color"],
                "label": config["label"],
                "users": card_data_list,
            }

        return directory

    @staticmethod
    def get_upper_manager(user):
        """مدیر بالادستی کاربر"""
        from apps.assessments.models import ScientificGroupMembership, ScientificGroup

        if user.is_staff or user.is_superuser:
            return None

        # اگه domain_manager هست → ادمین
        if ScientificGroupMembership.objects.filter(
            user=user, role="domain_manager", is_active=True
        ).exists():
            admins = User.objects.filter(is_staff=True).exclude(id=user.id)
            if admins.exists():
                return UserDirectoryService.get_user_card_data(
                    admins.first(),
                    role_label="ادمین سیستم",
                    role_color="danger",
                )

        # اگه scientific_manager هست → domain_manager همون حوزه
        if ScientificGroupMembership.objects.filter(
            user=user, role="scientific_manager", is_active=True
        ).exists():
            my_groups = list(ScientificGroupMembership.objects.filter(
                user=user, is_active=True
            ).values_list("scientific_group_id", flat=True))

            all_ids = list(my_groups)
            for gid in my_groups:
                group = ScientificGroup.objects.get(id=gid)
                if group.parent:
                    all_ids.append(group.parent_id)

            domain_manager = User.objects.filter(
                scientific_group_memberships__scientific_group_id__in=all_ids,
                scientific_group_memberships__role="domain_manager",
                scientific_group_memberships__is_active=True,
            ).exclude(id=user.id).first()

            if domain_manager:
                return UserDirectoryService.get_user_card_data(
                    domain_manager,
                    role_label="مدیر کل",
                    role_color="primary",
                )

        # اگه طراح یا دانشجو → مدیر علمی
        my_groups = list(ScientificGroupMembership.objects.filter(
            user=user, is_active=True
        ).values_list("scientific_group_id", flat=True))

        all_group_ids = list(my_groups)
        for gid in my_groups:
            parents = ScientificGroup.objects.filter(children__id=gid).values_list('id', flat=True)
            all_group_ids.extend(parents)

        scientific_manager = User.objects.filter(
            scientific_group_memberships__scientific_group_id__in=all_group_ids,
            scientific_group_memberships__role="scientific_manager",
            scientific_group_memberships__is_active=True,
        ).exclude(id=user.id).first()

        if scientific_manager:
            return UserDirectoryService.get_user_card_data(
                scientific_manager,
                role_label="مدیر علمی",
                role_color="info",
            )

        return None

    @staticmethod
    def replace_role(old_user, new_user, role, group_id):
        """انتقال نقش از old_user به new_user"""
        from apps.assessments.models import ScientificGroupMembership

        # غیرفعال کردن نقش old_user
        ScientificGroupMembership.objects.filter(
            user=old_user,
            scientific_group_id=group_id,
            role=role,
            is_active=True,
        ).update(is_active=False)

        # فعال/ساخت نقش new_user
        membership, created = ScientificGroupMembership.objects.get_or_create(
            user=new_user,
            scientific_group_id=group_id,
            role=role,
            defaults={"is_active": True},
        )
        if not created:
            membership.is_active = True
            membership.save()

        # چک کن old_user هنوز نقش دیگه‌ای داره؟
        has_other_roles = ScientificGroupMembership.objects.filter(
            user=old_user,
            is_active=True,
        ).exists()

        return {
            "old_user_is_guest": not has_other_roles,
            "membership": membership,
        }
