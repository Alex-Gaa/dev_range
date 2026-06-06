#C:\Users\Developer\PycharmProjects\devrange\users\views.py
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, ProfileSerializer, \
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer, VerifyEmailSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
from .models import (
    PasswordResetCode,
    EmailVerificationCode
)

from django.core.mail import send_mail


class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        code = (
            EmailVerificationCode
            .generate_code()
        )

        EmailVerificationCode.objects.create(
            user=user,
            code=code
        )
        verify_link = (
            f"{settings.FRONTEND_URL}"
            f"/verify-email"
            f"?email={user.email}"
            f"&code={code}"
        )

        send_mail(
            subject="Verify your email",
            message=(
                f"Verification code: {code}\n\n"
                f"Or open:\n{verify_link}"
            ),
            from_email=None,
            recipient_list=[user.email]
        )

        return Response(
            {
                "detail":
                "Account created. Check your email."
            },
            status=201
        )



class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "profile": ProfileSerializer(user.profile).data
        })

    # 🔥 ДОБАВЬ ЭТО
    def patch(self, request):
        user = request.user

        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.save()

        return Response({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "profile": ProfileSerializer(user.profile).data
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "logged out"})
        except Exception:
            return Response({"error": "invalid token"}, status=400)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

class PasswordResetRequestView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = (
            PasswordResetRequestSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data[
            "email"
        ]

        try:
            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "detail":
                    "If account exists, email was sent."
                }
            )

        code = PasswordResetCode.generate_code()

        PasswordResetCode.objects.create(
            user=user,
            code=code
        )
        reset_link = (
            f"{settings.FRONTEND_URL}"
            f"/reset-password"
            f"?email={email}"
            f"&code={code}"
        )

        send_mail(
            subject="Password reset",
            message=(
                f"Use this code: {code}\n\n"
                f"Or open:\n{reset_link}"
            ),
            from_email=None,
            recipient_list=[email]
        )

        return Response({
            "detail":
            "If account exists, email was sent."
        })

class PasswordResetConfirmView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = (
            PasswordResetConfirmSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.validated_data

        try:

            user = User.objects.get(
                email=data["email"]
            )

        except User.DoesNotExist:

            return Response(
                {
                    "detail": "Invalid code"
                },
                status=400
            )

        reset = (
            PasswordResetCode.objects
            .filter(
                user=user,
                code=data["code"],
                is_used=False
            )
            .order_by("-created_at")
            .first()
        )

        if not reset:
            return Response(
                {
                    "detail": "Invalid code"
                },
                status=400
            )

        if reset.is_expired:
            return Response(
                {
                    "detail": "Code expired"
                },
                status=400
            )

        user.set_password(
            data["password"]
        )

        user.save()

        reset.is_used = True
        reset.save()

        return Response({
            "detail":
            "Password changed successfully"
        })

class VerifyEmailView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            return Response({"detail": "Invalid code"}, status=400)

        verification = (
            EmailVerificationCode.objects
            .filter(user=user, code=data["code"], is_used=False)
            .order_by("-created_at")
            .first()
        )

        if not verification:
            return Response({"detail": "Invalid code"}, status=400)

        if verification.is_expired:
            return Response({"detail": "Code expired"}, status=400)

        # 🔥 если уже верифицирован — просто логиним снова (НЕ ошибка)
        if user.is_verified:
            EmailVerificationCode.objects.filter(
                user=user,
                is_used=False
            ).update(is_used=True)

            refresh = RefreshToken.for_user(user)

            return Response({
                "detail": "Email already verified",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role,
                    "first_name": user.first_name,
                }
            })

        # verify user
        user.is_verified = True
        user.save()

        verification.is_used = True
        verification.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "detail": "Email verified successfully",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
            }
        })