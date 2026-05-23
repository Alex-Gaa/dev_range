from django.contrib import admin

from billing.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "plan",
        "status",
        "lessons_used",
        "expires_at",
    )

    search_fields = (
        "user__email",
    )