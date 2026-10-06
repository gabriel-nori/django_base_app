from config.settings import LOG_LEVEL, LOG_TO_DB
from datetime import datetime
import json

log_level_index_ids = {"debug": 0, "info": 1, "warning": 2, "error": 3, "critical": 4}


class Logger:
    app_name: str = None
    level = LOG_LEVEL.lower()
    level_index = 0

    def __init__(self, app_name, override_level: str = None) -> None:
        self.app_name = app_name

        if override_level:
            self.level = override_level.lower()

        self.level_index = log_level_index_ids[self.level.lower()]

    def debug(self, message: str, extra: dict = None, trace=None):
        level = "debug"
        if self.level_index <= log_level_index_ids[level]:
            self.__log__(message, level, extra, trace=trace)

    def info(self, message: str, extra: dict = None, trace=None):
        level = "info"
        if self.level_index <= log_level_index_ids[level]:
            self.__log__(message, level, extra, trace=trace)

    def warning(self, message: str, extra: dict = None, trace=None):
        level = "warning"
        if self.level_index <= log_level_index_ids[level]:
            self.__log__(message, level, extra, trace=trace)

    def error(self, message: str, extra: dict = None, trace=None):
        level = "error"
        if self.level_index <= log_level_index_ids[level]:
            self.__log__(message, level, extra, trace=trace)

    def critical(self, message: str, extra: dict = None, trace=None):
        level = "critical"
        if self.level_index <= log_level_index_ids[level]:
            self.__log__(message, level, extra, trace=trace)

    def __log__(self, message: str, level: str, extra: dict = None, trace=None):
        log_message = {
            "timestamp": str(datetime.now()),
            "app_name": self.app_name,
            "log_level": level,
            "trace": None if trace is None else str(trace),
            "message": message,
            "extra": extra,
        }
        print(json.dumps(log_message, indent=2, default=str))

        if LOG_TO_DB:
            self.__persist__(log_message)

    def __persist__(self, log_message: dict):
        """Save the entry in AppLog. A logging failure never breaks the caller."""
        from django.apps import apps as django_apps

        if not django_apps.ready:
            return

        try:
            from apps.logs.models import AppLog

            AppLog.objects.create(
                app_name=log_message["app_name"],
                level=log_message["log_level"],
                message=str(log_message["message"]),
                # Round trip so non JSON values (datetime, UUID...) become strings
                extra=json.loads(json.dumps(log_message["extra"], default=str)),
                trace=log_message["trace"],
            )
        except Exception as error:
            print(
                json.dumps(
                    {
                        "timestamp": str(datetime.now()),
                        "app_name": "logger",
                        "log_level": "error",
                        "message": "Failed to persist log in database",
                        "extra": {"error": str(error)},
                    },
                    indent=2,
                )
            )
