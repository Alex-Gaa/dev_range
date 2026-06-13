from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

users = User.objects.filter(username__startswith="user")[:10000]

tokens = []

for user in users:
    refresh = RefreshToken.for_user(user)
    tokens.append(str(refresh.access_token))

file_path = r"C:\Users\Developer\PycharmProjects\devrange\billing\tests\tokens.txt"

with open(file_path, "w") as f:
    f.write("\n".join(tokens))

print("TOKENS GENERATED:", len(tokens))