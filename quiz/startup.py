import os
from django.contrib.auth import get_user_model

def create_default_admin():
    User = get_user_model()
    username = os.getenv("ADMIN_USERNAME", "admin")
    password = os.getenv("ADMIN_PASSWORD", "admin123")
    email = os.getenv("ADMIN_EMAIL", "admin@example.com")

    if not User.objects.filter(username=username).exists():
        print(f"Creating default admin: {username}")
        user = User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print("Default admin already exists.")
