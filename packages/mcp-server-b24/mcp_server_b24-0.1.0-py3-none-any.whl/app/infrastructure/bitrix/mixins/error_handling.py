"""
Модуль с миксином для обработки ошибок Bitrix24 API.

Содержит общие методы и функции для обработки ошибок при работе с API Bitrix24.
"""

from collections.abc import Awaitable, Callable
from typing import Any

from app.infrastructure.logging.logger import logger


class BitrixErrorHandlingMixin:
    """
    Миксин для обработки ошибок при работе с Bitrix24 API.

    Предоставляет методы для безопасного выполнения API запросов
    с обработкой ошибок.
    """

    @classmethod
    async def _safe_call[T_Result](  # noqa: PLR0911
        cls,
        func: Callable[..., Awaitable[T_Result]],
        error_message: str,
        default_value: T_Result,
        *args: Any,
        **kwargs: Any,
    ) -> T_Result:
        """
        Безопасное выполнение функции с обработкой ошибок.

        :param func: Функция для выполнения
        :param error_message: Сообщение при ошибке
        :param default_value: Значение по умолчанию при ошибке
        :param args: Позиционные аргументы для функции
        :param kwargs: Именованные аргументы для функции
        :returns: Результат выполнения функции или значение по умолчанию
        """
        try:
            return await func(*args, **kwargs)
        except ConnectionError:
            logger.error(f"{error_message}: ошибка соединения")
            return default_value
        except TimeoutError:
            logger.error(f"{error_message}: превышено время ожидания")
            return default_value
        except ValueError as e:
            logger.error(f"{error_message}: некорректное значение: {e}")
            return default_value
        except KeyError as e:
            logger.error(f"{error_message}: отсутствует ключ: {e}")
            return default_value
        except AttributeError as e:
            logger.error(f"{error_message}: ошибка атрибута: {e}")
            return default_value
        except RuntimeError as e:
            logger.error(f"{error_message}: ошибка выполнения: {e}")
            return default_value
        except Exception as e:
            logger.error(f"{error_message}: неожиданная ошибка: {e}")
            return default_value

    @staticmethod
    def _format_entity_name(entity_class: Any) -> str:
        """
        Форматирование имени сущности для логирования.

        :param entity_class: Класс сущности
        :returns: Отформатированное имя сущности
        """
        if hasattr(entity_class, "__name__"):
            return entity_class.__name__
        return str(entity_class)
