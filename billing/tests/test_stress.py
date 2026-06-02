from django.test import TestCase
from django.contrib.auth import get_user_model

from billing.services import (
    activate_subscription,
    can_generate_lesson,
    increment_lessons_usage,
)

from children.models import Child
from lessons.models import Lesson

User = get_user_model()


class BillingStressTest(TestCase):

    def create_parent(self, email, plan):

        parent = User.objects.create_user(
            username=email,
            email=email,
            password="test123",
            role="parent",
            first_name="Test",
            last_name="User",
        )

        activate_subscription(parent, plan)

        return parent

    def create_children(self, parent, limit):

        created = 0

        for i in range(limit + 2):

            if Child.objects.filter(parent=parent).count() >= limit:
                break

            Child.objects.create(
                parent=parent,
                first_name=f"Child {i}",
                age=10,
                grade="5",
            )

            created += 1

        return created

    def create_lessons(self, parent, child, limit):

        created = 0

        for i in range(limit + 10):

            if not can_generate_lesson(parent):
                break

            Lesson.objects.create(
                child=child,
                title=f"Lesson {i}",
                content={},
            )

            increment_lessons_usage(parent)

            created += 1

        return created

    def test_free_plan(self):

        parent = self.create_parent(
            "free@test.com",
            "free"
        )

        children = self.create_children(parent, 1)

        child = Child.objects.get(parent=parent)

        lessons = self.create_lessons(parent, child, 5)

        self.assertEqual(children, 1)
        self.assertEqual(lessons, 5)

    def test_basic_plan(self):

        parent = self.create_parent(
            "basic@test.com",
            "basic"
        )

        children = self.create_children(parent, 1)

        child = Child.objects.get(parent=parent)

        lessons = self.create_lessons(parent, child, 50)

        self.assertEqual(children, 1)
        self.assertEqual(lessons, 50)

    def test_family_plan(self):

        parent = self.create_parent(
            "family@test.com",
            "family"
        )

        children = self.create_children(parent, 3)

        child = Child.objects.filter(
            parent=parent
        ).first()

        lessons = self.create_lessons(parent, child, 200)

        self.assertEqual(children, 3)
        self.assertEqual(lessons, 200)