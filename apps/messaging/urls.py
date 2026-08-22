from django.urls import path

from apps.messaging.views import (
    ConversationDetailView,
    StudentConversationView,
    InstructorConversationView,
    ConversationInboxView,
    MessageFileView,
)


app_name = "messaging"


urlpatterns = [

    path(
        "conversation/<int:conversation_id>/",
        ConversationDetailView.as_view(),
        name="conversation-detail",
    ),
    path(
        "student/conversation/<int:assignment_id>/",
        StudentConversationView.as_view(),
        name="student-conversation",
    ),
    path(
        "instructor/conversation/<int:assignment_id>/",
        InstructorConversationView.as_view(),
        name="instructor-conversation",
    ),
    path(
        "inbox/",
        ConversationInboxView.as_view(),
        name="inbox",
    ),
    path(
        "file/<int:message_id>/",
        MessageFileView.as_view(),
        name="message-file",
    ),

]