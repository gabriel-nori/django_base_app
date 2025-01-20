from app.config import settings
from datetime import datetime
import json

log_level_index_ids = {
    "debug": 0,
    "info": 1,
    "warning": 2,
    "error": 3,
    "critical": 4
}

class Logger:
    app_name: str = None
    level = settings.LOG_LEVEL.lower()
    level_index = 0

    def __init__(self, app_name, override_level: str = None) -> None:
        self.app_name = app_name

        if override_level:
            self.level = override_level.lower()

        self.level_index = log_level_index_ids[self.level.lower()]

    def debug(self, message: str, extra: dict = None, trace = None):
        level = "debug"
        if self.level_index <= log_level_index_ids[level]:
            self.__log__(message, level, extra, trace = None)

    def info(self, message: str, extra: dict = None, trace = None):
        level = "info"
        if self.level_index <= log_level_index_ids[level]:
            self.__log__(message, level, extra, trace = None)

    def warning(self, message: str, extra: dict = None, trace = None):
        level = "warning"
        if self.level_index <= log_level_index_ids[level]:
            self.__log__(message, level, extra, trace = None)

    def error(self, message: str, extra: dict = None, trace = None):
        level = "error"
        if self.level_index <= log_level_index_ids[level]:
            self.__log__(message, level, extra, trace = None)

    def critical(self, message: str, extra: dict = None, trace = None):
        level = "critical"
        if self.level_index <= log_level_index_ids[level]:
            self.__log__(message, level, extra, trace = None)

    def __log__(self, message: str, level: str, extra: dict = None, trace = None):
        log_message = {
            "timestamp": str(datetime.now()),
            "app_name": self.app_name,
            "log_level": level,
            "trace": trace,
            "message": message,
            "extra": extra
        }
        print(json.dumps(log_message, indent=2))