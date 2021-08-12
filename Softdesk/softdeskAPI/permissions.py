from rest_framework import permissions

from .models import Contributor, Project


def get_project(view):
    if "project_pk" in view.kwargs:
        project_pk = view.kwargs["project_pk"]
    else:
        project_pk = view.kwargs["pk"]
    return Project.objects.get(pk=project_pk)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author_id == request.user


class HasCreatedProjectOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a project to edit or delete it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        contributor = Contributor.objects.get(user_id=request.user, project_id=get_project(view))
        return contributor.role == "author"


# class IsProjectCreatorOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow authors of a project to edit or delete it.
#     """
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.role == "author"


class IsContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors of a project to see it.
    """
    def has_permission(self, request, view):
        return Contributor.objects.filter(user_id=request.user, project_id=get_project(view)).exists()
