# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# DISCLAIMER: This software is provided "as is" without any warranty,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose, and non-infringement.
#
# In no event shall the authors or copyright holders be liable for any
# claim, damages, or other liability, whether in an action of contract,
# tort, or otherwise, arising from, out of, or in connection with the
# software or the use or other dealings in the software.
# -----------------------------------------------------------------------------

# @Author  : Tek Raj Chhetri
# @Email   : tekraj@mit.edu
# @Web     : https://tekrajchhetri.com/
# @File    : configure_logging.py
# @Software: PyCharm

from logging.config import dictConfig
from core.configuration import config, DevelopmentConfig

handlers = ["default", "rotating_file"]
if config.ENV_STATE == "prod":
    handlers = ["default", "rotating_file", "logtail"] #if we don't want to store logs in logtail then it can be removed


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if isinstance(config, DevelopmentConfig) else 32,
                    "default_value": "-",
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s %(msecs)03d %(levelname)s %(correlation_id)s %(name)s %(lineno)d %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id"],
                },
                "logtail": {
                    "class": "logtail.LogtailHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id"],
                    "source_token": config.LOGTAIL_API_KEY,
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filters": ["correlation_id"],
                    "filename": "storeapi.log",
                    "maxBytes": 1024 * 1024 * 40,  # 40 MB each file
                    "backupCount": 2,  # total number of files you want to keep after that the file will be deleted
                    "encoding": "utf8",
                },
            },
            "loggers": {
                "uvicorn": {
                    "handlers": ["default", "rotating_file", "logtail"],
                    "level": "INFO",
                },
                "storeapi": {
                    "handlers": handlers,
                    "level": (
                        "DEBUG" if isinstance(config, DevelopmentConfig) else "INFO"
                    ),
                    "propogate": False,
                },
                "databases": {
                    "handlers": ["default"],
                    "level": "WARNING",
                },
                "aiosqlite": {
                    "handlers": ["default"],
                    "level": "WARNING",
                },
            },
        }
    )
