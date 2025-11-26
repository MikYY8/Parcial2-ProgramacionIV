from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create default superuser on Render"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.environ.get("RENDER_SU_NAME")
        email = os.environ.get("RENDER_SU_EMAIL")
        password = os.environ.get("RENDER_SU_PASSWORD")

        if not username or not password:
            self.stdout.write("Superuser env vars not set. Skipping.")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superuser {username} already exists.")
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(f"Superuser {username} created successfully.")