"""
Модуль для централизованной настройки логирования с использованием structlog.

Предоставляет структурированное логирование для всего приложения.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

import structlog
from structlog.stdlib import LoggerFactory

from app.config import settings

logging.getLogger("fast_bitrix24").addHandler(logging.StreamHandler())
logging.getLogger("fast_bitrix24").setLevel(logging.WARNING)


def setup_logging() -> structlog.stdlib.BoundLogger:
    """
    Настройка структурированного логирования с использованием structlog.

    :returns: Настроенный structlog логгер
    """
    logging.basicConfig(
        format="%(message)s",
        level=settings.LOG_LEVEL,
        handlers=[],
    )

    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(console_handler)

    if hasattr(settings, "LOG_FILE") and settings.LOG_FILE:
        log_file = Path(settings.LOG_FILE)
        log_dir = log_file.parent

        if log_dir and not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
        )
        root_logger.addHandler(file_handler)

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    structlog.configure(
        processors=[*processors, structlog.dev.ConsoleRenderer()],
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


def bind_logger(**context: Any) -> structlog.stdlib.BoundLogger:
    """
    Создает новый контекстно-связанный логгер.

    :param context: Контекст, который будет добавлен к логам
    :returns: Контекстно-связанный логгер
    """
    return logger.bind(**context)


logger = setup_logging()
