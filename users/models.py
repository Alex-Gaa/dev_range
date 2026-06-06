#C:\Users\Developer\PycharmProjects\devrange\users\models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random

class User(AbstractUser):
    class Role(models.TextChoices):
        PARENT = "parent", "Parent"
        CHILD = "child", "Child"
        TEACHER = "teacher", "Teacher"
        ADMIN = "admin", "Admin"

    username = models.CharField(max_length=150, unique=True)  # оставляем для Django

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PARENT
    )

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Profile(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="profile")

    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    bio = models.TextField(blank=True, null=True)

    location = models.CharField(max_length=255, blank=True, null=True)

    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    telegram_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

class PasswordResetCode(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_reset_codes"
    )

    code = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_used = models.BooleanField(
        default=False
    )

    @property
    def is_expired(self):
        return (
            timezone.now()
            >
            self.created_at + timedelta(minutes=15)
        )

    @staticmethod
    def generate_code():
        return str(
            random.randint(
                100000,
                999999
            )
        )