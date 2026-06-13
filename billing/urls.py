#C:\Users\Developer\PycharmProjects\devrange\billing\urls.py
from django.urls import path

from billing.views import TestUpgradeView, SubscriptionView, ActivateSubscriptionView, CreatePaymentView, \
    SimulatePaymentSuccessView

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
    path("create-payment/", CreatePaymentView.as_view()),
    path("simulate-success/", SimulatePaymentSuccessView.as_view()),
]