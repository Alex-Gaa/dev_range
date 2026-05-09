# lessons/admin.py
from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "child",
        "status",
        "created_at",
    )

    list_filter = ("status", "created_at")
    search_fields = ("title", "child__first_name")

    ordering = ("-created_at",)