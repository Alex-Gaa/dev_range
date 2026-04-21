#C:\Users\Developer\PycharmProjects\devrange\users\urls.py
from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, MeView, UpdateProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),

    path("me/", MeView.as_view()),
    path("profile/", UpdateProfileView.as_view()),
]