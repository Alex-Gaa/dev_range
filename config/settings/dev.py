from .base import *

DEBUG = True

SECRET_KEY = "django-dev-key"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
)