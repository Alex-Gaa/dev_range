#C:\Users\Developer\PycharmProjects\devrange\config\settings\prod.py
from .base import *
import os

DEBUG = False

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

FRONTEND_URL = os.getenv("FRONTEND_URL")

CORS_ALLOWED_ORIGINS = [FRONTEND_URL] if FRONTEND_URL else []

CSRF_TRUSTED_ORIGINS = [FRONTEND_URL] if FRONTEND_URL else []

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https"
)

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
