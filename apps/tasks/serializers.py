from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "is_completed",
            "created_at",
            "updated_at",
            "owner",
        )
        read_only_fields = ("id", "created_at", "updated_at", "owner")

