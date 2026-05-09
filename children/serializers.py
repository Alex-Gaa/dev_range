from rest_framework import serializers

from .models import Child


class ChildSerializer(serializers.ModelSerializer):

    invite_link = serializers.ReadOnlyField()

    class Meta:
        model = Child

        fields = (
            "id",
            "first_name",
            "age",
            "grade",
            "interests",
            "avatar",
            "has_account",
            "invite_link",
            "created_at",
        )

        read_only_fields = (
            "invite_link",
            "created_at",
        )