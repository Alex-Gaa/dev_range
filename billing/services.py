# C:\Users\Developer\PycharmProjects\devrange\billing\services.py

from datetime import timedelta

from django.utils import timezone

from billing.models import Subscription


def get_or_create_subscription(user):

    subscription, _ = Subscription.objects.get_or_create(
        user=user
    )

    return subscription


def activate_subscription(user, plan):

    subscription = get_or_create_subscription(user)

    subscription.plan = plan
    subscription.status = "active"

    subscription.lessons_used = 0

    subscription.expires_at = (
        timezone.now() + timedelta(days=30)
    )

    subscription.save()

    return subscription


def can_generate_lesson(user):

    subscription = get_or_create_subscription(user)

    from billing.constants import PLANS

    limit = PLANS[subscription.plan]["lessons_limit"]

    return subscription.lessons_used < limit


def increment_lessons_usage(user):

    subscription = get_or_create_subscription(user)

    subscription.lessons_used += 1

    subscription.save()