#C:\Users\Developer\PycharmProjects\devrange\lessons\models.py
from django.conf import settings
from django.db import models
from children.models import Child


class Lesson(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(max_length=255)

    content = models.JSONField(default=dict)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    progress = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.child.first_name})"

class Subject(models.Model):

    name = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True
    )

    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    is_global = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

class Topic(models.Model):

    subject = models.ForeignKey(
        Subject,
        related_name="topics",
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

