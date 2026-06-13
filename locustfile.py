#C:\Users\Developer\PycharmProjects\devrange\locustfile.py
from locust import HttpUser, task, between
import random


class SaaSUser(HttpUser):
    wait_time = between(2, 4)

    # ======================
    # INIT
    # ======================
    def on_start(self):
        self.token = None
        self.children = []
        self.logged_in = False

        self.login()
        if not self.logged_in:
            return

        self.load_children()

    # ======================
    # LOGIN (safe + measured)
    # ======================
    def login(self):
        with self.client.post(
            "/api/auth/login/",
            json={
                "username": "test1@test.ru",
                "password": "Asdf2020"
            },
            name="/api/auth/login/",
            catch_response=True
        ) as response:

            if response.status_code != 200:
                response.failure(f"LOGIN FAILED {response.status_code}")
                return

            try:
                self.token = response.json().get("access")
                if not self.token:
                    response.failure("NO TOKEN")
                    return

                self.client.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })

                self.logged_in = True
                response.success()

            except Exception as e:
                response.failure(str(e))

    # ======================
    # LOAD CHILDREN
    # ======================
    def load_children(self):
        with self.client.get(
            "/api/children/",
            name="/api/children/",
            catch_response=True
        ) as response:

            if response.status_code != 200:
                response.failure("FAILED LOAD CHILDREN")
                return

            try:
                data = response.json()
                if isinstance(data, list):
                    self.children = data
                response.success()

            except Exception as e:
                response.failure(str(e))

    # ======================
    # HELPERS
    # ======================
    def pick_child(self):
        if not self.children:
            return None
        return random.choice(self.children).get("id")

    def safe(self):
        return self.logged_in and self.token is not None

    # ======================
    # SCENARIO 1: READ HEAVY (real users)
    # ======================
    @task(5)
    def get_lessons(self):
        if not self.safe():
            return

        self.client.get(
            "/api/lessons/",
            name="/api/lessons/"
        )

    # ======================
    # SCENARIO 2: CREATE LESSON (low frequency)
    # ======================
    @task(2)
    def create_lesson(self):
        if not self.safe():
            return

        child_id = self.pick_child()
        if not child_id:
            return

        with self.client.post(
            "/api/lessons/",
            json={
                "child": child_id,
                "title": "Load Test Lesson",
                "content": {
                    "theory": "test"
                }
            },
            name="/api/lessons/",
            catch_response=True
        ) as response:

            if response.status_code >= 400:
                response.failure(response.text)
            else:
                response.success()

    # ======================
    # SCENARIO 3: SUBSCRIPTION CHECK (light)
    # ======================
    @task(1)
    def check_subscription(self):
        if not self.safe():
            return

        self.client.get(
            "/api/billing/subscription/",
            name="/api/billing/subscription/"
        )

    # ======================
    # OPTIONAL STRESS ENDPOINT (uncomment if needed)
    # ======================
    # @task(1)
    # def stress_lessons_read(self):
    #     if not self.safe():
    #         return
    #
    #     self.client.get(
    #         "/api/lessons/?limit=50",
    #         name="/api/lessons?limit=50"
    #     )