from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CreateUserAPIView, ProjectViewSet, ProjectDetailViewSet, ProjectContributorsViewSet, \
    RemoveContributorAPIView, ProjectIssuesViewSet, ProjectIssuesUpdateAndDeleteViewSet, ProjectIssueCommentsViewSet, \
    ProjectIssueCommentsDetailsViewSet

projects = ProjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

project_details = ProjectDetailViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

project_contributors = ProjectContributorsViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

project_issues = ProjectIssuesViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

project_issues_change = ProjectIssuesUpdateAndDeleteViewSet.as_view({
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
project_issue_comments = ProjectIssueCommentsViewSet.as_view({
    'post': 'create',
    'get': 'list'
})
project_issue_comments_details = ProjectIssueCommentsDetailsViewSet.as_view({
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
    'get': 'retrieve'
})

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view(), name='create_user'),
    path('projects/', projects, name='projects'),
    path('projects/<int:pk>/', project_details, name='project_details'),
    path('projects/<int:pk>/users/', project_contributors, name='project_contributors'),
    path('projects/<int:project_pk>/users/<int:pk>/', RemoveContributorAPIView.as_view(),
         name='remove_project_contributor'),
    path('projects/<int:project_pk>/issues/', project_issues, name="project_issues"),
    path('projects/<int:project_pk>/issues/<int:pk>/', project_issues_change, name="change_project_issues"),
    path('projects/<int:project_pk>/issues/<int:pk>/comments/', project_issue_comments, name="comments"),
    path('projects/<int:project_pk>/issues/<int:issue_pk>/comments/<int:pk>', project_issue_comments_details,
         name="comments_details"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
