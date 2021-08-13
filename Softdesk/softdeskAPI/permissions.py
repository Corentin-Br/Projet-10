from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from .models import Contributor, Project


def get_project(view):
    project_pk = view.kwargs["project_pk"] if "project_pk" in view.kwargs else view.kwargs["pk"]
    return get_object_or_404(Project, pk=project_pk)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class HasCreatedProjectOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a project to edit or delete it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        contributor = Contributor.objects.get(user=request.user, project=get_project(view))
        return contributor.role == "author"


class IsContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors of a project to see it.
    """
    def has_permission(self, request, view):
        return Contributor.objects.filter(user=request.user, project=get_project(view)).exists()
