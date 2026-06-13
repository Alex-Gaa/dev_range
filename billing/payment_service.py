# billing/payment_service.py

from django.db import transaction
from billing.models import Payment
from billing.constants import PLANS
from billing.services import activate_subscription
import uuid
def create_payment(user, plan):

    if plan not in PLANS:
        raise ValueError("Unknown plan")

    payment = Payment.objects.create(
        user=user,
        plan=plan,
        amount=PLANS[plan]["price"],
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
            return None  # или raise ValidationError("Payment not found")

        # 🔥 идемпотентность (ключевой момент)
        if payment.status == Payment.STATUS_SUCCEEDED:
            return payment

        payment.status = Payment.STATUS_SUCCEEDED
        payment.save()

        # активируем подписку
        activate_subscription(
            user=payment.user,
            plan=payment.plan
        )

    return payment

