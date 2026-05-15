#C:\Users\Developer\PycharmProjects\devrange\children\models.py
from uuid import uuid4
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone


class Child(models.Model):

    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="children"
    )

    # OPTIONAL CHILD ACCOUNT
    linked_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child_profile"
    )

    # BASIC INFO
    first_name = models.CharField(max_length=255)

    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    age = models.PositiveIntegerField()

    grade = models.CharField(max_length=50)

    interests = models.TextField(
        blank=True,
        null=True
    )

    avatar = models.ImageField(
        upload_to="children/avatars/",
        blank=True,
        null=True
    )

    # ACCOUNT SYSTEM
    has_account = models.BooleanField(default=False)

    invite_token = models.UUIDField(
        unique=True,
        null=True,
        blank=True
    )

    invite_expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        # GENERATE INVITE TOKEN
        if self.has_account and not self.invite_token:

            self.invite_token = uuid4()

            self.invite_expires_at = (
                timezone.now() + timedelta(days=7)
            )

        super().save(*args, **kwargs)

    @property
    def invite_link(self):

        if not self.invite_token:
            return None

        return f"/child-invite/{self.invite_token}"

    @property
    def is_invite_valid(self):

        if not self.invite_expires_at:
            return False

        return timezone.now() < self.invite_expires_at

    def __str__(self):

        return f"{self.first_name} ({self.age})"