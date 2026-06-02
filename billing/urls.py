#C:\Users\Developer\PycharmProjects\devrange\billing\urls.py
from django.urls import path

from billing.views import TestUpgradeView, SubscriptionView, ActivateSubscriptionView

urlpatterns = [
    path(
        "test-upgrade/",
        TestUpgradeView.as_view()
    ),
    path(
        "subscription/",
        SubscriptionView.as_view()
    ),

    path(
        "activate/",
        ActivateSubscriptionView.as_view()
    ),
]