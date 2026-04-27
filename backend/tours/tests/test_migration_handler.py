from unittest.mock import patch

from django.test import SimpleTestCase

from migration_handler import handler


class MigrationHandlerTests(SimpleTestCase):
    @patch("migration_handler.call_command")
    @patch("migration_handler.django.setup")
    def test_handler_runs_migrate_with_default_database(self, mock_setup, mock_call_command):
        response = handler({}, None)

        mock_setup.assert_called_once_with()
        mock_call_command.assert_called_once_with(
            "migrate",
            interactive=False,
            database="default",
            verbosity=1,
        )
        self.assertEqual(
            response,
            {
                "ok": True,
                "command": "migrate",
                "database": "default",
            },
        )

    @patch("migration_handler.call_command")
    @patch("migration_handler.django.setup")
    def test_handler_accepts_database_override(self, mock_setup, mock_call_command):
        response = handler({"database": "replica", "verbosity": 2}, None)

        mock_setup.assert_called_once_with()
        mock_call_command.assert_called_once_with(
            "migrate",
            interactive=False,
            database="replica",
            verbosity=2,
        )
        self.assertEqual(response["database"], "replica")
