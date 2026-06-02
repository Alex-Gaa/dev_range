#C:\Users\Developer\PycharmProjects\devrange\billing\models.py
from django.db import models
from django.conf import settings


class Subscription(models.Model):

    PLAN_CHOICES = [
        ("free", "Free"),
        ("basic", "Basic"),
        ("family", "Family"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("expired", "Expired"),
        ("cancelled", "Cancelled"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    plan = models.CharField(
        max_length=30,
        choices=PLAN_CHOICES,
        default="free"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="active"
    )

    lessons_used = models.IntegerField(
        default=0
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.plan}"