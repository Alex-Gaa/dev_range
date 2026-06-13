#C:\Users\Developer\PycharmProjects\devrange\billing\views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from billing.payment_service import create_payment, handle_success_payment
from billing.serializers import SubscriptionSerializer
from billing.services import activate_subscription, get_or_create_subscription


class TestUpgradeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != "parent":
            raise PermissionDenied(
                "Only parents can manage subscriptions."
            )
        plan = request.data.get("plan")

        subscription = activate_subscription(
            request.user,
            plan
        )

        return Response({
            "detail": "Subscription activated",
            "plan": subscription.plan,
            "expires_at": subscription.expires_at,
        })


class SubscriptionView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):
        if request.user.role != "parent":
            raise PermissionDenied(
                "Only parents can view subscription."
            )

        subscription = (
            get_or_create_subscription(
                request.user
            )
        )

        serializer = SubscriptionSerializer(
            subscription
        )

        return Response(serializer.data)


class ActivateSubscriptionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != "parent":
            raise PermissionDenied(
                "Only parents can manage subscriptions."
            )

        plan = request.data.get(
            "plan",
            "basic"
        )

        subscription = activate_subscription(
            request.user,
            plan
        )

        serializer = SubscriptionSerializer(
            subscription
        )

        return Response(serializer.data)

class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        plan = request.data.get("plan")

        payment = create_payment(request.user, plan)

        return Response({
            "payment_id": payment.provider_payment_id,
            "status": payment.status,
            "amount": payment.amount,
        })

class SimulatePaymentSuccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        payment_id = request.data.get("payment_id")

        payment = handle_success_payment(payment_id)

        subscription = get_or_create_subscription(request.user)

        return Response({
            "status": payment.status,
            "plan": payment.plan,
            "subscription": subscription.plan
        })