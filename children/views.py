# C:\Users\Developer\PycharmProjects\devrange\children\views.py

from rest_framework import generics, status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Child
from .serializers import (
    ChildSerializer,
    AcceptInviteSerializer,
)

from rest_framework.exceptions import ValidationError

from billing.services import reserve_lesson, get_or_create_subscription, is_subscription_active

from billing.constants import PLANS

from django.contrib.auth.password_validation import (
    validate_password
)
import secrets
import string


# =========================================
# CHILDREN LIST / CREATE
# =========================================

class ChildListCreateView(generics.ListCreateAPIView):

    serializer_class = ChildSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Child.objects.filter(
            parent=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):

        if not is_subscription_active(
                self.request.user
        ):
            raise ValidationError({
                "detail":
                    "Subscription is inactive or expired."
            })

        subscription = get_or_create_subscription(
            self.request.user
        )

        limit = PLANS[
            subscription.plan
        ]["children_limit"]

        current_count = Child.objects.filter(
            parent=self.request.user
        ).count()

        if current_count >= limit:
            raise ValidationError({
                "detail":
                    f"Your {subscription.plan} plan allows only {limit} children."
            })

        serializer.save(
            parent=self.request.user
        )


# =========================================
# INVITE DETAILS
# =========================================

class ChildInviteDetailView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, token):

        try:

            child = Child.objects.get(
                invite_token=token
            )

        except Child.DoesNotExist:

            return Response(
                {
                    "error": "Invalid invite"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not child.is_invite_valid:

            return Response(
                {
                    "error": "Invite expired"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "first_name": child.first_name,
            "last_name": child.last_name,
            "email": child.email,
            "grade": child.grade,
        })


# =========================================
# ACCEPT INVITE
# =========================================

class AcceptInviteView(generics.CreateAPIView):

    serializer_class = AcceptInviteSerializer

    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                "message": "Child account created",
                "email": user.email,
            },
            status=status.HTTP_201_CREATED
        )

# 🔥 NEW
class ChildDetailView(generics.RetrieveAPIView):
    serializer_class = ChildSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Child.objects.filter(parent=self.request.user)

class ResetChildPasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:

            child = Child.objects.get(
                id=pk,
                parent=request.user
            )

        except Child.DoesNotExist:

            return Response(
                {
                    "detail": "Child not found"
                },
                status=404
            )

        if not child.linked_user:

            return Response(
                {
                    "detail":
                    "Child has no account"
                },
                status=400
            )

        alphabet = (
            string.ascii_letters +
            string.digits +
            "!@#$%^&*"
        )

        while True:

            password = "".join(
                secrets.choice(alphabet)
                for _ in range(12)
            )

            try:

                validate_password(
                    password,
                    child.linked_user
                )

                break

            except Exception:
                continue

        child.linked_user.set_password(
            password
        )

        child.linked_user.save()

        return Response({
            "new_password": password
        })