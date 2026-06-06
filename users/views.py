#C:\Users\Developer\PycharmProjects\devrange\users\views.py
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .models import PasswordResetCode
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, ProfileSerializer, \
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


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