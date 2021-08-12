from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import MyUser, Project, Contributor, Issue, Comment
from .permissions import IsContributor, HasCreatedProjectOrReadOnly, IsAuthorOrReadOnly, get_project
from .serializers import MyUserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer


class CreateUserAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MyUserSerializer


class ProjectViewSet(ListModelMixin,
                     CreateModelMixin,
                     GenericViewSet):
    # permission_classes = [IsAuthenticated,]
    serializer_class = ProjectSerializer

    def get_queryset(self, **kwargs):
        return [contributor.project_id for contributor in self.request.user.contributors_id.all()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        contributor = ContributorSerializer(data={
            'user_id': request.user.id,
            'project_id': Project.objects.all().last().id,
            'permission': "perm",  # Placeholder
            'role': "author"
        })
        contributor.is_valid(raise_exception=True)
        contributor.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectDetailViewSet(RetrieveModelMixin,
                           UpdateModelMixin,
                           DestroyModelMixin,
                           GenericViewSet):

    permission_classes = [IsContributor, HasCreatedProjectOrReadOnly]  # IsAuthenticated,
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProjectContributorsViewSet(ListModelMixin,
                                 CreateModelMixin,
                                 DestroyModelMixin,
                                 GenericViewSet):

    permission_classes = [IsContributor, HasCreatedProjectOrReadOnly]
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return get_project(self).contributors_id

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["project_id"] = Project.objects.get(pk=self.kwargs["pk"]).id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RemoveContributorAPIView(DestroyAPIView):
    permission_classes = [IsContributor, HasCreatedProjectOrReadOnly]

    def get_queryset(self):
        return get_project(self).contributors_id


class ProjectIssuesViewSet(ListModelMixin,
                           CreateModelMixin,
                           GenericViewSet):
    permission_classes = [IsContributor, IsAuthorOrReadOnly]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return get_project(self).issues_id

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["project_id"] = Project.objects.get(pk=self.kwargs["project_pk"]).id
        data["author_id"] = request.user.id
        data["assignee_id"] = data.get("assignee_id", request.user.id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectIssuesUpdateAndDeleteViewSet(UpdateModelMixin,
                                          DestroyModelMixin,
                                          GenericViewSet):
    permission_classes = [IsContributor, IsAuthorOrReadOnly]
    serializer_class = IssueSerializer

    def get_queryset(self, **kwargs):
        return get_project(self).issues_id


class ProjectIssueCommentsViewSet(CreateModelMixin,
                                  ListModelMixin,
                                  GenericViewSet):
    permission_classes = [IsContributor, IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self, **kwargs):
        return get_object_or_404(Issue, pk=self.kwargs["pk"]).comments_id

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["issue_id"] = Issue.objects.get(pk=self.kwargs["pk"]).id
        data["author_id"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectIssueCommentsDetailsViewSet(UpdateModelMixin,
                                         DestroyModelMixin,
                                         RetrieveModelMixin,
                                         GenericViewSet):
    permission_classes = [IsContributor, IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self, **kwargs):
        return get_object_or_404(Issue, pk=self.kwargs["issue_pk"]).comments_id
