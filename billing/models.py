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

    plan = models.CharField(max_length=30, choices=PLAN_CHOICES, default="free")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="active")

    lessons_used = models.IntegerField(default=0)

    expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan}"



class Payment(models.Model):

    STATUS_PENDING = "pending"
    STATUS_SUCCEEDED = "succeeded"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_SUCCEEDED, "Succeeded"),
        (STATUS_FAILED, "Failed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    plan = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    provider_payment_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )

    # ✅ FIX 1: ИДЕМПОТЕНТНОСТЬ WEBHOOK
    processed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)