import random
import time
from concurrent.futures import ThreadPoolExecutor

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from faker import Faker

from billing.services import (
    activate_subscription,
    can_generate_lesson,
    increment_lessons_usage,
)

from billing.constants import PLANS
from children.models import Child
from lessons.models import Lesson, Subject

fake = Faker()

User = get_user_model()


class Command(BaseCommand):

    help = "Realistic SaaS load test"

    def handle(self, *args, **kwargs):

        self.stdout.write("\n🔥 START LOAD TEST 🔥\n")

        start = time.time()

        users = self.create_users(50)

        self.stdout.write(f"Users created: {len(users)}")

        with ThreadPoolExecutor(max_workers=10) as executor:

            for user in users:

                executor.submit(self.simulate_user, user)

        end = time.time()

        self.stdout.write("\n======================")
        self.stdout.write(f"TOTAL TIME: {end - start:.2f}s")
        self.stdout.write("======================\n")

    # -----------------------------
    # CREATE USERS
    # -----------------------------
    def create_users(self, count):

        users = []

        plans = list(PLANS.keys())

        for i in range(count):

            user = User.objects.create_user(
                username=f"user{i}@test.com",
                email=f"user{i}@test.com",
                password="test123",
                role="parent",
            )

            plan = random.choice(plans)

            activate_subscription(user, plan)

            users.append(user)

        return users

    # -----------------------------
    # SIMULATE REAL USER
    # -----------------------------
    def simulate_user(self, user):

        try:

            plan = user.subscription.plan

            limits = PLANS[plan]

            # CREATE CHILDREN
            children = []

            for i in range(limits["children_limit"] + 2):

                if Child.objects.filter(parent=user).count() >= limits["children_limit"]:
                    break

                child = Child.objects.create(
                    parent=user,
                    first_name=fake.first_name(),
                    age=random.randint(6, 15),
                    grade="5",
                )

                children.append(child)

            if not children:
                return

            child = children[0]

            # CREATE SUBJECT
            subject = Subject.objects.create(
                name="Math",
                parent=user,
                slug=f"math-{user.id}",
            )

            # CREATE LESSONS
            created = 0

            for i in range(limits["lessons_limit"] + 10):

                if not can_generate_lesson(user):
                    break

                Lesson.objects.create(
                    child=child,
                    subject=subject,
                    title=fake.sentence(),
                    content={},
                )

                increment_lessons_usage(user)

                created += 1

            self.stdout.write(
                f"{user.email}: lessons={created}"
            )

        except Exception as e:

            self.stdout.write(
                self.style.ERROR(
                    f"{user.email}: ERROR {str(e)}"
                )
            )