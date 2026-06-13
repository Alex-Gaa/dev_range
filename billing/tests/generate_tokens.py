import requests

BASE_URL = "http://127.0.0.1:8000"

TOKENS = []

# =========================
# 1. CREATE USERS FIRST
# =========================
for i in range(1000):
    username = f"user{i}@test.ru"
    password = "Asdf2020!"

    # регистрация (если есть endpoint)
    requests.post(
        f"{BASE_URL}/api/auth/register/",
        json={
            "email": username,
            "username": username,
            "password": password
        }
    )

    # login
    r = requests.post(
        f"{BASE_URL}/api/auth/login/",
        json={
            "username": username,
            "password": password
        }
    )

    if r.status_code == 200:
        token = r.json().get("access")
        if token:
            TOKENS.append(token)

# =========================
# 2. SAVE TOKENS
# =========================
with open("tokens.txt", "w", encoding="utf-8") as f:
    for t in TOKENS:
        f.write(t + "\n")

print(f"Generated {len(TOKENS)} tokens")