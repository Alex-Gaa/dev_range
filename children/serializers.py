#C:\Users\Developer\PycharmProjects\devrange\children\serializers.py
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Child
User = get_user_model()

class ChildSerializer(serializers.ModelSerializer):

    invite_link = serializers.ReadOnlyField()

    class Meta:
        model = Child

        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
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
# =========================================
# ACCEPT CHILD INVITE
# =========================================

class AcceptInviteSerializer(serializers.Serializer):

    token = serializers.UUIDField()

    email = serializers.EmailField()

    password = serializers.CharField(write_only=True)

    password2 = serializers.CharField(write_only=True)

    first_name = serializers.CharField()

    last_name = serializers.CharField()

    def validate(self, attrs):

        # PASSWORD CHECK
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                "Passwords do not match"
            )

        validate_password(attrs["password"])

        # INVITE CHECK
        try:
            child = Child.objects.get(
                invite_token=attrs["token"]
            )
        except Child.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid invite token"
            )

        # EXPIRED CHECK
        if not child.is_invite_valid:
            raise serializers.ValidationError(
                "Invite link expired"
            )

        # ALREADY LINKED
        if child.linked_user:
            raise serializers.ValidationError(
                "Child already linked"
            )

        attrs["child"] = child

        return attrs

    def create(self, validated_data):

        child = validated_data["child"]

        # CREATE CHILD USER
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=User.Role.CHILD,
        )

        # LINK USER TO CHILD
        child.linked_user = user

        # CLEAR INVITE
        child.invite_token = None
        child.invite_expires_at = None

        child.save()

        return user