from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views import View

from apps.education.models import InstructorAssignment
from apps.messaging.services.messaging_service import (
    MessagingService,
)


class StudentConversationView(
    LoginRequiredMixin,
    View,
):

    def get(
        self,
        request,
        assignment_id,
    ):

        assignment = (
            InstructorAssignment.objects
            .select_related(
                "student",
                "instructor",
                "learning_path",
            )
            .get(
                id=assignment_id,
                student=request.user,
                is_active=True,
            )
        )

        conversation = (
            MessagingService
            .get_or_create_conversation(
                student=assignment.student,
                instructor=assignment.instructor,
                learning_path=assignment.learning_path,
                assignment=assignment,
            )
        )

        return redirect(
            "messaging:conversation-detail",
            conversation_id=conversation.id,
        )