from django.test import TestCase, override_settings
from django.conf import settings
from apps.logs.models import AppLog
from unittest import mock
from logger import Logger
import datetime


@mock.patch("builtins.print")
class LoggerDatabaseTestCase(TestCase):
    def test_does_not_persist_when_disabled(self, _print):
        with mock.patch("logger.LOG_TO_DB", False):
            Logger("tests").info("not saved")
        self.assertFalse(AppLog.objects.exists())

    def test_persists_when_enabled(self, _print):
        with mock.patch("logger.LOG_TO_DB", True):
            Logger("tests").error(
                "saved",
                extra={"when": datetime.date(2026, 1, 1), "count": 1},
                trace="Traceback...",
            )
        log = AppLog.objects.get()
        self.assertEqual(log.app_name, "tests")
        self.assertEqual(log.level, AppLog.Level.ERROR)
        self.assertEqual(log.message, "saved")
        self.assertEqual(log.extra, {"when": "2026-01-01", "count": 1})
        self.assertEqual(log.trace, "Traceback...")

    def test_respects_log_level(self, _print):
        with mock.patch("logger.LOG_TO_DB", True):
            Logger("tests", override_level="warning").info("below level")
        self.assertFalse(AppLog.objects.exists())

    def test_database_failure_does_not_raise(self, _print):
        with mock.patch("logger.LOG_TO_DB", True), mock.patch(
            "apps.logs.models.AppLog.objects.create", side_effect=RuntimeError("db down")
        ):
            Logger("tests").info("still fine")


@mock.patch("builtins.print")
@override_settings(
    MIDDLEWARE=settings.MIDDLEWARE + ["apps.logs.middleware.RequestLogMiddleware"]
)
class RequestLogMiddlewareTestCase(TestCase):
    def test_logs_api_requests(self, _print):
        with mock.patch("logger.LOG_TO_DB", True):
            self.client.get("/api/private/users/me/")
        log = AppLog.objects.get()
        self.assertEqual(log.app_name, "request")
        self.assertEqual(log.level, AppLog.Level.WARNING)
        self.assertEqual(log.extra["status"], 401)
        self.assertEqual(log.extra["path"], "/api/private/users/me/")
        self.assertIsNone(log.extra["user_id"])

    def test_ignores_non_api_requests(self, _print):
        with mock.patch("logger.LOG_TO_DB", True):
            self.client.get("/not-an-api-route/")
        self.assertFalse(AppLog.objects.exists())
