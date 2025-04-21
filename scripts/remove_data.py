import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FolkloreManagementSystem.settings")
django.setup()

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Wipes all data from the entire database (⚠ irreversible)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("⚠ WIPING ALL DATA from database..."))

        models = apps.get_models()
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("SET session_replication_role = 'replica';")  # Disable FK checks

                for model in models:
                    table = model._meta.db_table
                    try:
                        cursor.execute(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE;')
                        self.stdout.write(self.style.NOTICE(f"🧼 Wiped: {table}"))
                    except Exception as e:
                        self.stderr.write(f"⚠ Could not wipe {table}: {e}")

                cursor.execute("SET session_replication_role = 'origin';")  # Re-enable FK checks

        self.stdout.write(self.style.SUCCESS(" All data wiped successfully."))

if __name__ == "__main__":
    Command().handle()