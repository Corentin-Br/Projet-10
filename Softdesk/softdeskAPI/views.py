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
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self, **kwargs):
        return [contributor.project for contributor in self.request.user.contributors.all()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        contributor = ContributorSerializer(data={
            'user': request.user.id,
            'project': Project.objects.all().last().id,
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

    permission_classes = [IsAuthenticated, IsContributor, HasCreatedProjectOrReadOnly]  # IsAuthenticated,
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProjectContributorsViewSet(ListModelMixin,
                                 CreateModelMixin,
                                 DestroyModelMixin,
                                 GenericViewSet):

    permission_classes = [IsAuthenticated, IsContributor, HasCreatedProjectOrReadOnly]
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return get_project(self).contributors

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["project"] = Project.objects.get(pk=self.kwargs["pk"]).id
        data["role"] = data.get("role", "contributor")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RemoveContributorAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsContributor, HasCreatedProjectOrReadOnly]

    def get_queryset(self):
        return get_project(self).contributors


class ProjectIssuesViewSet(ListModelMixin,
                           CreateModelMixin,
                           GenericViewSet):
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return get_project(self).issues

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["project"] = Project.objects.get(pk=self.kwargs["project_pk"]).id
        data["author"] = request.user.id
        data["assignee"] = data.get("assignee", request.user.id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectIssuesUpdateAndDeleteViewSet(UpdateModelMixin,
                                          DestroyModelMixin,
                                          GenericViewSet):
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    serializer_class = IssueSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data["project"] = instance.project.id
        data["author"] = instance.author.id
        data["assignee"] = data.get("assignee", instance.assignee).id
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_queryset(self, **kwargs):
        return get_project(self).issues


class ProjectIssueCommentsViewSet(CreateModelMixin,
                                  ListModelMixin,
                                  GenericViewSet):
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self, **kwargs):
        return get_object_or_404(Issue, pk=self.kwargs["pk"]).comments

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["issue"] = Issue.objects.get(pk=self.kwargs["pk"]).id
        data["author"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectIssueCommentsDetailsViewSet(UpdateModelMixin,
                                         DestroyModelMixin,
                                         RetrieveModelMixin,
                                         GenericViewSet):
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self, **kwargs):
        return get_object_or_404(Issue, pk=self.kwargs["issue_pk"]).comments

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data["issue"] = instance.issue.id
        data["author"] = instance.author.id
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
