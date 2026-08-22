from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from apps.accounts.mixins import InstructorRequiredMixin
from apps.education.models import InstructorAssignment
from apps.messaging.services.messaging_service import (
    MessagingService,
)


class InstructorConversationView(
    InstructorRequiredMixin,
    View,
):

    def get(
        self,
        request,
        assignment_id,
    ):

        assignment = get_object_or_404(
            InstructorAssignment.objects.select_related(
                "student",
                "instructor",
                "learning_path",
            ),
            id=assignment_id,
            instructor=request.user,
            is_active=True,
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