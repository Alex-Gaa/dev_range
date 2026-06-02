from locust import HttpUser, task, between
import random


class SaaSUser(HttpUser):
    wait_time = between(2, 5)

    def on_start(self):
        """Init user safely"""

        # 🔥 SAFE DEFAULTS (важно)
        self.token = None
        self.logged_in = False
        self.children = []

        # ======================
        # LOGIN
        # ======================
        login = self.client.post(
            "/api/auth/login/",
            json={
                "username": "test1@test.ru",
                "password": "Asdf2020"
            },
            name="/api/auth/login/"
        )

        if login.status_code != 200:
            print("LOGIN FAILED:", login.status_code, login.text)
            return

        self.token = login.json().get("access")
        self.logged_in = True

        # set auth header globally for user
        self.client.headers.update({
            "Authorization": f"Bearer {self.token}"
        })

        # ======================
        # LOAD CHILDREN
        # ======================
        try:
            children_resp = self.client.get(
                "/api/children/",
                name="/api/children/"
            )

            if children_resp.status_code == 200:
                data = children_resp.json()
                if isinstance(data, list):
                    self.children = data

        except Exception as e:
            print("CHILD LOAD ERROR:", e)

    # ======================
    # HELPERS
    # ======================
    def pick_child(self):
        if not self.children:
            return None
        return random.choice(self.children)["id"]

    def safe(self):
        return getattr(self, "logged_in", False) and self.token

    # ======================
    # REAL USER SCENARIOS
    # ======================

    @task(4)
    def get_lessons(self):
        if not self.safe():
            return

        self.client.get(
            "/api/lessons/",
            name="/api/lessons/"
        )

    @task(3)
    def create_lesson(self):
        if not self.safe():
            return

        child_id = self.pick_child()
        if not child_id:
            return

        response = self.client.post(
            "/api/lessons/",
            json={
                "child": child_id,
                "title": "Load Test Lesson",
                "content": {
                    "theory": "test"
                }
            },
            name="/api/lessons/"
        )

        if response.status_code >= 400:
            print("CREATE LESSON ERROR:", response.status_code, response.text)

    @task(2)
    def check_subscription(self):
        if not self.safe():
            return

        self.client.get(
            "/api/billing/subscription/",
            name="/api/billing/subscription/"
        )