# billing/services.py

from datetime import timedelta

from django.utils import timezone
from django.db import transaction

from billing.models import Subscription
from billing.constants import PLANS


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


def can_generate_lesson(user):

    subscription = get_or_create_subscription(user)

    if not is_subscription_active(user):
        return False

    limit = PLANS[
        subscription.plan
    ]["lessons_limit"]

    return (
        subscription.lessons_used < limit
    )


@transaction.atomic
def reserve_lesson(user):

    subscription = (
        Subscription.objects
        .select_for_update()
        .get(user=user)
    )

    if subscription.status != "active":
        return False

    if (
        subscription.expires_at
        and subscription.expires_at < timezone.now()
    ):
        return False

    limit = PLANS[
        subscription.plan
    ]["lessons_limit"]

    if subscription.lessons_used >= limit:
        return False

    subscription.lessons_used += 1

    subscription.save(
        update_fields=["lessons_used"]
    )

    return True

@transaction.atomic
def increment_lessons_usage(user):

    subscription = (
        Subscription.objects
        .select_for_update()
        .get(user=user)
    )

    subscription.lessons_used += 1

    subscription.save(
        update_fields=["lessons_used"]
    )

    return subscription

