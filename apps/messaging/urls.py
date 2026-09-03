from django.urls import path

from apps.messaging.views import (
    ConversationDetailView,
    StudentConversationView,
    InstructorConversationView,
    ConversationInboxView,
    MessageFileView,
)
from apps.messaging.views.direct_message import (
    DirectInboxView,
    DirectComposeView,
    DirectConversationView,
)
from apps.messaging.views.ticket import TicketCreateView
from apps.messaging.views.ticket_list import TicketListView
from apps.messaging.views.ticket import TicketCreateView
from apps.messaging.views.ticket_list import TicketListView


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
    path(
        "direct/",
        DirectInboxView.as_view(),
        name="direct-inbox",
    ),
    path(
        "direct/compose/",
        DirectComposeView.as_view(),
        name="direct-compose",
    ),
    path(
        "direct/conversation/<int:user_id>/",
        DirectConversationView.as_view(),
        name="direct-conversation",
    ),
    path(
        "ticket/create/",
        TicketCreateView.as_view(),
        name="ticket-create",
    ),
    path(
        "tickets/",
        TicketListView.as_view(),
        name="ticket-list",
    ),
    path(
        "ticket/create/",
        TicketCreateView.as_view(),
        name="ticket-create",
    ),
    path(
        "tickets/",
        TicketListView.as_view(),
        name="ticket-list",
    ),

]