from django.core.management.base import BaseCommand

# Idempotent functions that create the base objects each app needs
# (statuses, types, default settings...). Use get_or_create inside them.
# Example: from apps.users.initializer import create_users_base_objects
INITIALIZERS = []


class Command(BaseCommand):
    help = "Create initial objects"

    def handle(self, *args, **options):
        self.stdout.write("Creating initial objects...")
        for initializer in INITIALIZERS:
            self.stdout.write(f"Running {initializer.__module__}.{initializer.__name__}...")
            initializer()
        self.stdout.write(self.style.SUCCESS("Objects created successfully"))
