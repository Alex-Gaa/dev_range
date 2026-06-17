from django.contrib import admin

from billing.models import Subscription, Payment


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


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "plan",
        "amount",
        "status",
        "provider_payment_id",
        "created_at",
    )

    list_filter = (
        "status",
        "plan",
        "created_at",
    )

    search_fields = (
        "user__email",
        "provider_payment_id",
    )

    readonly_fields = (
        "provider_payment_id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)