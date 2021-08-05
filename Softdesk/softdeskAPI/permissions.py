from rest_framework import permissions

from Softdesk.softdeskAPI.models import Contributor


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

    def has_object_permission(self, request, view, project):
        if request.method in permissions.SAFE_METHODS:
            return True
        contributor = Contributor.objects.get(user=request.user, project=project)
        # contributor = [contributor for contributor in request.user.contributors if contributor.project == project]
        # return contributor[0].role if contributor else False
        return contributor.role == "creator"


class IsContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors of a project to see it.
    """
    def has_object_permission(self, request, view, project):
        return Contributor.objects.filter(user=request.user, project=project).exists()
