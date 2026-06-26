# billing/serializers.py

from rest_framework import serializers
from billing.models import Subscription, Plan

class SubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.SerializerMethodField()
    plan_price = serializers.SerializerMethodField()
    children_limit = serializers.SerializerMethodField()
    lessons_limit = serializers.SerializerMethodField()
    subjects_limit = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = "__all__"

    def _plan(self, obj):
        return Plan.objects.filter(
            code=obj.plan,
            is_active=True
        ).first()

    def get_plan_name(self, obj):
        plan = self._plan(obj)
        return plan.name if plan else obj.plan

    def get_plan_price(self, obj):
        plan = self._plan(obj)
        return plan.price if plan else 0

    def get_children_limit(self, obj):
        plan = self._plan(obj)
        return plan.children_limit if plan else 0

    def get_lessons_limit(self, obj):
        plan = self._plan(obj)
        return plan.lessons_limit if plan else 0

    def get_subjects_limit(self, obj):
        plan = self._plan(obj)
        return plan.subjects_limit if plan else 0