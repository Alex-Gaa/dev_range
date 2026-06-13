import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from billing.models import Payment, Subscription

User = get_user_model()


@pytest.mark.django_db
def test_full_billing_flow():
    client = APIClient()

    # -------------------------
    # 1. создаем пользователя
    # -------------------------
    user = User.objects.create_user(
        username="test1",
        email="test1@test.ru",
        password="Asdf2020!"
    )

    user.role = User.Role.PARENT
    user.save()

    client.force_authenticate(user=user)

    # -------------------------
    # 2. создаем payment
    # -------------------------
    response = client.post(
        "/api/billing/create-payment/",
        {"plan": "basic"},
        format="json"
    )

    assert response.status_code == 200

    payment_id = response.data["payment_id"]

    payment = Payment.objects.get(provider_payment_id=payment_id)

    assert payment.status == Payment.STATUS_PENDING
    assert payment.plan == "basic"

    # -------------------------
    # 3. симуляция webhook (успех оплаты)
    # -------------------------
    response = client.post(
        "/api/billing/simulate-success/",
        {"payment_id": payment_id},
        format="json"
    )

    assert response.status_code == 200

    payment.refresh_from_db()
    subscription = Subscription.objects.get(user=user)

    # -------------------------
    # 4. проверяем payment
    # -------------------------
    assert payment.status == Payment.STATUS_SUCCEEDED

    # -------------------------
    # 5. проверяем subscription
    # -------------------------
    assert subscription.plan == "basic"
    assert subscription.status == "active"
    assert subscription.lessons_used == 0
    assert subscription.expires_at is not None

    # -------------------------
    # 6. проверка идемпотентности (повторный webhook)
    # -------------------------
    response = client.post(
        "/api/billing/simulate-success/",
        {"payment_id": payment_id},
        format="json"
    )

    assert response.status_code == 200

    subscription.refresh_from_db()

    # ничего не должно измениться второй раз
    assert subscription.plan == "basic"
    assert subscription.lessons_used == 0

@pytest.mark.django_db
def test_subscription_limits():
    from billing.services import reserve_lesson

    user = User.objects.create_user(
        username="test1",
        email="test1@test.ru",
        password="Asdf2020!"
    )

    user.role = User.Role.PARENT
    user.save()

    sub = Subscription.objects.create(
        user=user,
        plan="free",
        status="active",
        lessons_used=0
    )

    # free = 5 lessons
    for i in range(5):
        assert reserve_lesson(user) is True

    # 6-й должен упасть
    assert reserve_lesson(user) is False

