import os

import django
from django.core.management import call_command


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")


def handler(event, context):
    django.setup()

    database = "default"
    verbosity = 1

    if isinstance(event, dict):
        raw_database = str(event.get("database", "")).strip()
        raw_verbosity = event.get("verbosity")

        if raw_database:
            database = raw_database

        if isinstance(raw_verbosity, int):
            verbosity = raw_verbosity

    call_command("migrate", interactive=False, database=database, verbosity=verbosity)

    return {
        "ok": True,
        "command": "migrate",
        "database": database,
    }
