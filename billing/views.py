#C:\Users\Developer\PycharmProjects\devrange\billing\views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
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