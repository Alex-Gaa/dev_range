#C:\Users\Developer\PycharmProjects\devrange\lessons\serializers.py

from rest_framework import serializers
from .models import Lesson, Subject, Topic


class LessonSerializer(serializers.ModelSerializer):

    child_name = serializers.CharField(
        source="child.first_name",
        read_only=True
    )

    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        required=False,
        allow_null=True
    )

    topic = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(),
        required=False,
        allow_null=True
    )

    subject_name = serializers.CharField(
        source="subject.name",
        read_only=True
    )

    topic_name = serializers.CharField(
        source="topic.name",
        read_only=True
    )

    class Meta:
        model = Lesson

        fields = [
            "id",
            "child",
            "child_name",

            "subject",
            "subject_name",

            "topic",
            "topic_name",

            "title",
            "content",
            "status",
            "progress",
            "created_at",
        ]
# lessons/serializers.py

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject

        fields = [
            "id",
            "name",
            "slug",
            "is_global",
        ]

        read_only_fields = [
            "slug",
            "is_global",
        ]
class TopicSerializer(serializers.ModelSerializer):

    subject_name = serializers.CharField(
        source="subject.name",
        read_only=True
    )

    class Meta:
        model = Topic
        fields = [
            "id",
            "name",
            "subject",
            "subject_name",
        ]