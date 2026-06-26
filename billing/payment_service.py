# billing/payment_service.py

import uuid

from django.db import transaction

from billing.models import Payment
from billing.services import (
    activate_subscription,
    get_plan,
)


def create_payment(user, plan_code):

    plan = get_plan(plan_code)

    if not plan:
        raise ValueError("Unknown plan")

    payment = Payment.objects.create(
        user=user,
        plan=plan.code,
        amount=plan.price,
        status=Payment.STATUS_PENDING,
        provider_payment_id=str(uuid.uuid4())
    )

    return payment


def handle_success_payment(provider_payment_id):

    with transaction.atomic():

        payment = (
            Payment.objects
            .select_for_update()
            .filter(provider_payment_id=provider_payment_id)
            .first()
        )

        if not payment:
            return None

        # уже обработан
        if payment.status == Payment.STATUS_SUCCEEDED:
            return payment

        payment.status = Payment.STATUS_SUCCEEDED
        payment.save()

        activate_subscription(
            user=payment.user,
            plan=payment.plan
        )

        return payment