from locust import HttpUser, task, between, events
import random
import os
from queue import Queue

TOKEN_FILE = os.path.join(os.path.dirname(__file__), "tokens.txt")

with open(TOKEN_FILE, "r", encoding="utf-8") as f:
    TOKENS = [t.strip() for t in f.readlines() if t.strip()]


# ======================================================
# GLOBAL QUEUE FOR REAL PAYMENT IDS
# ======================================================
payment_queue = Queue()


# ======================================================
# 1. HEAVY WRITER (creates payments)
# ======================================================
class PaymentCreatorUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.token = random.choice(TOKENS)

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    @task
    def create_payment(self):
        plan = random.choice(["basic", "family", "free"])

        with self.client.post(
            "/api/billing/create-payment/",
            json={"plan": plan},
            headers=self.headers(),
            name="create_payment",
            catch_response=True
        ) as response:

            if response.status_code != 200:
                response.failure(response.text[:200])
                return

            try:
                data = response.json()
                payment_id = data.get("payment_id")

                if payment_id:
                    payment_queue.put(payment_id)

                response.success()

            except Exception:
                response.failure("INVALID JSON")


# ======================================================
# 2. WEBHOOK SIMULATOR (REAL idempotency test)
# ======================================================
class WebhookUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.token = random.choice(TOKENS)

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    @task
    def webhook(self):

        if payment_queue.empty():
            return

        payment_id = payment_queue.get()

        # simulate retry storm
        for _ in range(2):
            self.client.post(
                "/api/billing/simulate-success/",
                json={"payment_id": payment_id},
                headers=self.headers(),
                name="webhook",
                catch_response=True
            )


# ======================================================
# 3. READ USERS (real traffic)
# ======================================================
class ReaderUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.token = random.choice(TOKENS)

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def subscription(self):
        self.client.get(
            "/api/billing/subscription/",
            headers=self.headers(),
            name="subscription"
        )

    @task(2)
    def lessons(self):
        self.client.get(
            "/api/lessons/",
            headers=self.headers(),
            name="lessons"
        )