from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from children.models import Child
from lessons.models import Subject

from billing.models import Subscription


class BillingLimitsTestCase(APITestCase):

    def setUp(self):

        self.parent = User.objects.create_user(
            username="parent@test.com",
            email="parent@test.com",
            password="test123456",
            role="parent",
            first_name="Parent",
            last_name="User",
        )

        self.client.force_authenticate(
            user=self.parent
        )

        self.subscription = Subscription.objects.create(
            user=self.parent,
            plan="free",
            status="active",
            lessons_used=0,
            expires_at=timezone.now() + timedelta(days=30)
        )

    def create_child(self):

        return self.client.post(
            "/api/children/",
            {
                "first_name": "Child",
                "last_name": "Test",
                "age": 10,
                "grade": "5",
            },
            format="json"
        )

    def create_subject(self, name):

        return self.client.post(
            "/api/lessons/subjects/",
            {
                "name": name
            },
            format="json"
        )

    def create_lesson(self, child_id, title):

        return self.client.post(
            "/api/lessons/",
            {
                "child": child_id,
                "title": title,
                "content": {
                    "theory": "test"
                }
            },
            format="json"
        )

    def test_free_plan_children_limit(self):

        response = self.create_child()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        response = self.create_child()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_free_plan_lessons_limit(self):

        child = Child.objects.create(
            parent=self.parent,
            first_name="Test",
            age=10,
            grade="5"
        )

        for i in range(5):

            response = self.create_lesson(
                child.id,
                f"Lesson {i}"
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED
            )

        response = self.create_lesson(
            child.id,
            "Lesson 6"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_expired_subscription_blocks_everything(self):

        self.subscription.expires_at = (
            timezone.now() - timedelta(days=1)
        )

        self.subscription.save()

        response = self.create_child()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_cancelled_subscription_blocks_everything(self):

        self.subscription.status = "cancelled"

        self.subscription.save()

        response = self.create_child()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_subject_limit_basic_plan(self):

        self.subscription.plan = "basic"

        self.subscription.save()

        self.create_subject("Math")
        self.create_subject("English")
        self.create_subject("Science")

        response = self.create_subject(
            "History"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )