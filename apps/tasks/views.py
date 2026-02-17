from rest_framework import permissions, viewsets

from .models import Task
from .serializers import TaskSerializer


class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only owners of a task to access it.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.owner == request.user


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

