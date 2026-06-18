#C:\Users\Developer\PycharmProjects\devrange\config\settings\prod.py
import os

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

FRONTEND_URL = os.getenv("FRONTEND_URL")

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL
] if FRONTEND_URL else []

CSRF_TRUSTED_ORIGINS = [
    FRONTEND_URL
] if FRONTEND_URL else []

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https"
)

# 🔥 ВАЖНО ДЛЯ HTTP (без домена и HTTPS)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
