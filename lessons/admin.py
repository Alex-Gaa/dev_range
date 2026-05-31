# lessons/admin.py

from django.contrib import admin

from .models import (
    Lesson,
    Subject,
    Topic,
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "parent",
        "is_global",
        "created_at",
    )

    list_filter = (
        "is_global",
        "created_at",
    )

    search_fields = (
        "name",
        "slug",
    )

    ordering = (
        "name",
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "subject",
        "created_at",
    )

    list_filter = (
        "subject",
        "created_at",
    )

    search_fields = (
        "name",
        "subject__name",
    )

    ordering = (
        "subject",
        "name",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "child",
        "subject",
        "topic",
        "status",
        "progress",
        "created_at",
    )

    list_filter = (
        "status",
        "subject",
        "topic",
        "created_at",
    )

    search_fields = (
        "title",
        "child__first_name",
        "subject__name",
        "topic__name",
    )

    autocomplete_fields = (
        "subject",
        "topic",
    )

    ordering = (
        "-created_at",
    )