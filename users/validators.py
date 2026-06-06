#C:\Users\Developer\PycharmProjects\devrange\users\validators.py
import re

from django.core.exceptions import ValidationError


class CustomPasswordValidator:

    def validate(self, password, user=None):

        if len(password) < 8:
            raise ValidationError(
                "Password must contain at least 8 characters."
            )

        if not re.search(r"[A-Z]", password):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", password):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", password):
            raise ValidationError(
                "Password must contain at least one digit."
            )

        if not re.search(r"[!@#$%^&*()_+=\-]", password):
            raise ValidationError(
                "Пароль должен содержать хотя бы один специальный символ."
            )

    def get_help_text(self):
        return (
            "Password must contain at least 8 characters, "
            "uppercase letter, lowercase letter, "
            "digit and special character."
        )