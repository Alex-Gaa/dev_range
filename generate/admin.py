from django.contrib import admin
from .models import AIPromptTemplate, GeneratedLessonMemory


@admin.register(AIPromptTemplate)
class AIPromptTemplateAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "is_active")
    list_filter = ("subject", "is_active")
    search_fields = ("subject", "name")


@admin.register(GeneratedLessonMemory)
class GeneratedLessonMemoryAdmin(admin.ModelAdmin):
    list_display = ("subject", "topic", "child", "created_at")
    list_filter = ("subject",)
    search_fields = ("subject", "topic")