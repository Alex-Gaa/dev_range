# billing/services.py

from datetime import timedelta

from django.utils import timezone
from django.db import transaction

from billing.models import Subscription
from billing.constants import PLANS
from django.db.models import F

def get_or_create_subscription(user):

    subscription, _ = Subscription.objects.get_or_create(
        user=user
    )

    return subscription


def activate_subscription(user, plan):

    if plan not in PLANS:
        raise ValueError(
            f"Unknown plan: {plan}"
        )

    subscription = get_or_create_subscription(user)

    subscription.plan = plan
    subscription.status = "active"

    subscription.lessons_used = 0

    subscription.expires_at = (
        timezone.now() + timedelta(days=30)
    )

    subscription.save()

    return subscription


def is_subscription_active(user):

    subscription = get_or_create_subscription(user)

    if subscription.status != "active":
        return False

    if (
        subscription.expires_at
        and subscription.expires_at < timezone.now()
    ):
        return False

    return True



@transaction.atomic
def reserve_lesson(user):

    subscription = get_or_create_subscription(user)

    subscription = (
        Subscription.objects
        .select_for_update()
        .get(pk=subscription.pk)
    )

    # check active
    if subscription.status != "active":
        return False

    if (
        subscription.expires_at
        and subscription.expires_at < timezone.now()
    ):
        return False

    limit = PLANS[subscription.plan]["lessons_limit"]

    # 🔥 IMPORTANT: atomic check + increment safe
    if subscription.lessons_used >= limit:
        return False

    Subscription.objects.filter(
        id=subscription.id
    ).update(
        lessons_used=F("lessons_used") + 1
    )

    return True


