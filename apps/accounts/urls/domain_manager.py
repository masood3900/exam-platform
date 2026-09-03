from django.urls import path

from apps.accounts.views.domain_manager.dashboard import DomainManagerDashboardView
from apps.accounts.views.domain_manager.learning_paths import DomainManagerLearningPathListView
from apps.accounts.views.domain_manager.learning_path_delete import DomainManagerLearningPathDeleteView
from apps.accounts.views.domain_manager.learning_path_create import DomainManagerLearningPathCreateView
from apps.accounts.views.domain_manager.assign_manager import DomainManagerAssignManagerView
from apps.accounts.views.domain_manager.user_directory import DomainManagerUserDirectoryView

app_name = "domain_manager"

urlpatterns = [
    path("dashboard/", DomainManagerDashboardView.as_view(), name="dashboard"),
    path("learning-paths/", DomainManagerLearningPathListView.as_view(), name="learning-paths"),
    path("learning-paths/create/", DomainManagerLearningPathCreateView.as_view(), name="learning-path-create"),
    path("learning-paths/<uuid:path_id>/assign-manager/", DomainManagerAssignManagerView.as_view(), name="assign-manager"),
    path("learning-paths/<uuid:path_id>/delete/", DomainManagerLearningPathDeleteView.as_view(), name="learning-path-delete"),
    path("users/", DomainManagerUserDirectoryView.as_view(), name="user-directory"),
]