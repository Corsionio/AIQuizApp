import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Creates a default admin user from environment variables"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.getenv("DJANGO_ADMIN_USERNAME")
        password = os.getenv("DJANGO_ADMIN_PASSWORD")
        email = os.getenv("DJANGO_ADMIN_EMAIL")

        if not all([username, password, email]):
            self.stdout.write(self.style.WARNING("Missing ADMIN_* environment variables"))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Admin user '{username}' created."))
        else:
            self.stdout.write(self.style.NOTICE(f"ℹ Admin user '{username}' already exists."))
