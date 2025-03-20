import logging
import logging.config

from pythonjsonlogger import jsonlogger

from .settings import settings


class CustomLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return True


class MixinLogFormatter:
    @staticmethod
    def mixin_record_format(record: logging.LogRecord):
        # record.user = 1
        # record.request_id = 100
        return record


class JsontLogFormatter(jsonlogger.JsonFormatter, MixinLogFormatter):
    def format(self, record: logging.LogRecord) -> str:
        record = self.mixin_record_format(record)
        return super().format(record)


class DefaultLogFormatter(logging.Formatter, MixinLogFormatter):
    def format(self, record: logging.LogRecord) -> str:
        record = self.mixin_record_format(record)
        return super().format(record)


MSG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
# MSG_FORMAT = '%(asctime)s %(name)s %(levelname)s %(message)s %(request_id)s %(user)s'
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "custom": {
            "()": CustomLogFilter,
        },
    },
    "formatters": {
        "json": {
            "()": JsontLogFormatter,
            "format": MSG_FORMAT,
        },
        "default": {
            "()": DefaultLogFormatter,
            "format": MSG_FORMAT,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json" if settings.JSON_LOGS else "default",
            "level": "INFO",
            "filters": ["custom"],
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "json",
            "filename": "project.log",
            "level": "DEBUG",
            "filters": ["custom"],
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
