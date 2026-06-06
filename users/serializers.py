#C:\Users\Developer\PycharmProjects\devrange\users\serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import Profile
from django.contrib.auth.password_validation import (
    validate_password
)
from django.core.exceptions import (
    ValidationError as DjangoValidationError
)


User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "role",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                "Passwords do not match"
            )

        try:
            validate_password(attrs["password"])

        except DjangoValidationError as e:
            raise serializers.ValidationError({
                "password": list(e.messages)
            })

        return attrs


    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["email"],  # внутренний username (не используем на фронте)
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data.get("role", "parent")
        )
        user.is_verified = False
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        user = User.objects.filter(
            email=attrs["username"]
        ).first()

        if user and not user.is_verified:
            raise serializers.ValidationError({
                "detail": "Email is not verified"
            })

        data = super().validate(attrs)

        user = self.user

        data["user"] = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        }

        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "avatar",
            "bio",
            "location",
            "github_url",
            "linkedin_url",
            "telegram_url",
            "portfolio_url",
        )


class PasswordResetRequestSerializer(
    serializers.Serializer
):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(
    serializers.Serializer
):
    email = serializers.EmailField()

    code = serializers.CharField()

    password = serializers.CharField()

    password2 = serializers.CharField()

    def validate(self, attrs):

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                "Passwords do not match"
            )

        try:
            validate_password(
                attrs["password"]
            )

        except DjangoValidationError as e:

            raise serializers.ValidationError({
                "password": list(e.messages)
            })

        return attrs

class VerifyEmailSerializer(
    serializers.Serializer
):

    email = serializers.EmailField()

    code = serializers.CharField()