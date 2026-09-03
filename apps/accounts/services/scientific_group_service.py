from apps.assessments.models import (
    ScientificGroup,
    ScientificGroupMembership,
    LearningObjective,
)


class ScientificGroupService:
    """سرویس جامع مدیریت گروه‌های علمی"""

    # ========== موضوع/دوره ==========

    @staticmethod
    def get_manager_fields(user):
        """رشته‌هایی که کاربر مدیر علمیشونه"""
        return ScientificGroup.objects.filter(
            memberships__user=user,
            memberships__role=ScientificGroupMembership.Role.SCIENTIFIC_MANAGER,
            memberships__is_active=True,
        ).distinct()

    @staticmethod
    def create_topic(name, code, description, parent_id):
        """ساخت موضوع/دوره"""
        parent = ScientificGroup.objects.get(id=parent_id)
        return ScientificGroup.objects.create(
            name=name,
            code=code,
            description=description,
            parent=parent,
        )

    @staticmethod
    def get_topics_of_field(field_id):
        """موضوع‌های یک رشته"""
        return ScientificGroup.objects.filter(
            parent_id=field_id,
            is_active=True,
        )

    # ========== اهداف آموزشی ==========

    @staticmethod
    def create_objective(name, code, description, topic_id):
        """ساخت هدف برای موضوع"""
        topic = ScientificGroup.objects.get(id=topic_id)
        return LearningObjective.objects.create(
            name=name,
            code=code,
            description=description,
            scientific_group=topic,
        )

    @staticmethod
    def get_topic_objectives(topic_id):
        """اهداف یک موضوع"""
        return LearningObjective.objects.filter(
            scientific_group_id=topic_id,
            is_active=True,
        )
    @staticmethod
    def create_topic_with_objectives_and_designers(
        name, code, description, parent_id, 
        objective_data_list, designer_ids
    ):
        """
        ساخت موضوع + اهداف + انتصاب طراحان
        objective_data_list = [{"name": "...", "code": "..."}, ...]
        designer_ids = [user_id, ...]
        """
        # ساخت موضوع
        topic = ScientificGroupService.create_topic(name, code, description, parent_id)
        
        # ساخت اهداف
        objectives = []
        for obj_data in objective_data_list:
            if obj_data.get("name", "").strip():
                obj = ScientificGroupService.create_objective(
                    name=obj_data["name"],
                    code=obj_data.get("code", ""),
                    description=obj_data.get("description", ""),
                    topic_id=str(topic.id),
                )
                objectives.append(obj)
        
        # انتصاب طراحان
        designers = []
        for user_id in designer_ids:
            if user_id:
                membership, created = ScientificGroupMembership.objects.get_or_create(
                    user_id=user_id,
                    scientific_group=topic,
                    role=ScientificGroupMembership.Role.QUESTION_DESIGNER,
                    defaults={"is_active": True},
                )
                if not created:
                    membership.is_active = True
                    membership.save()
                designers.append(membership)
        
        return {
            "topic": topic,
            "objectives": objectives,
            "designers": designers,
        }