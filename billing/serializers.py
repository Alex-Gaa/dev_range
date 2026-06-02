#C:\Users\Developer\PycharmProjects\devrange\billing\serializers.py
from rest_framework import serializers

from billing.models import Subscription


class SubscriptionSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Subscription

        fields = "__all__"