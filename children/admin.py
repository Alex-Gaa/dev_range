# children/admin.py
from django.contrib import admin
from .models import Child


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "age", "grade", "parent")
    search_fields = ("first_name", "parent__email")
    list_filter = ("grade",)