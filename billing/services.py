# billing/services.py

from datetime import timedelta

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from rest_framework.exceptions import ValidationError

from billing.models import Subscription
from billing.constants import PLANS


def get_or_create_subscription(user):
    """
    Atomic-safe creation (important under load)
    """
    subscription, _ = Subscription.objects.get_or_create(
        user=user,
        defaults={
            "plan": "free",
            "status": "active",
            "lessons_used": 0,
        }
    )
    return subscription


def activate_subscription(user, plan):
    if plan not in PLANS:
        raise ValidationError({"detail": f"Unknown plan: {plan}"})

    with transaction.atomic():
        subscription, _ = Subscription.objects.select_for_update().get_or_create(
            user=user,
            defaults={
                "plan": plan,
                "status": "active",
                "lessons_used": 0,
                "expires_at": timezone.now() + timedelta(days=30),
            }
        )

        subscription.plan = plan
        subscription.status = "active"
        subscription.lessons_used = 0
        subscription.expires_at = timezone.now() + timedelta(days=30)
        subscription.save()

        return subscription


def is_subscription_active(user):
    sub = Subscription.objects.filter(user=user).first()

    if not sub:
        return False

    if sub.status != "active":
        return False

    if sub.expires_at and sub.expires_at < timezone.now():
        return False

    return True


@transaction.atomic
def reserve_lesson(user):
    """
    FULL SAFE VERSION:
    - no double reservation
    - no race condition
    - safe under Locust load
    """

    subscription = Subscription.objects.select_for_update().get(user=user)

    # expired / inactive
    if subscription.status != "active":
        return False

    if subscription.expires_at and subscription.expires_at < timezone.now():
        return False

    limit = PLANS[subscription.plan]["lessons_limit"]

    # atomic check + update
    updated = Subscription.objects.filter(
        id=subscription.id,
        lessons_used__lt=limit,
        status="active"
    ).update(
        lessons_used=F("lessons_used") + 1
    )

    return updated == 1