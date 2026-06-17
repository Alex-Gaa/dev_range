#C:\Users\Developer\PycharmProjects\devrange\config\settings\dev.py
from .base import *

DEBUG = True

SECRET_KEY = "django-dev-key"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    '72.56.34.59',
]

CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)