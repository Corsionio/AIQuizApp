import os
from django.contrib.auth import get_user_model

def create_default_admin():
    User = get_user_model()

    username = os.getenv("DJANGO_ADMIN_USERNAME")
    password = os.getenv("DJANGO_ADMIN_PASSWORD")
    email = os.getenv("DJANGO_ADMIN_EMAIL")

    # Only proceed if all environment variables are set
    if not all([username, password, email]):
        print("Skipping admin creation: Missing DJANGO_ADMIN_USERNAME, DJANGO_ADMIN_PASSWORD, or DJANGO_ADMIN_EMAIL")
        return

    if not User.objects.filter(username=username).exists():
        print(f"Creating default admin: {username}")
        User.objects.create_superuser(username=username, password=password, email=email)
    else:
        print(f"Admin user '{username}' already exists.")

