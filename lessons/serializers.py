#C:\Users\Developer\PycharmProjects\devrange\lessons\serializers.py

from rest_framework import serializers
from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):

    child_name = serializers.CharField(
        source="child.first_name",
        read_only=True
    )

    class Meta:
        model = Lesson

        fields = [
            "id",
            "child",
            "child_name",
            "title",
            "content",
            "status",
            "progress",
            "created_at",
        ]