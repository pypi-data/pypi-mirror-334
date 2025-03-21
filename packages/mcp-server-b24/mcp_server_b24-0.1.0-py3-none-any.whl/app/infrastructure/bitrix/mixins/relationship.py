"""
Модуль с миксином для работы со связями между сущностями Bitrix24.

Содержит методы для управления отношениями между сущностями (контакты-компании,
сделки-контакты и т.д.).
"""

from typing import Any, ClassVar

from fast_bitrix24 import Bitrix

from app.infrastructure.logging.logger import logger


class BitrixRelationshipMixin:
    """
    Миксин для работы со связями между сущностями в Bitrix24.

    Предоставляет методы для управления отношениями между сущностями
    (контакты-компании, сделки-контакты и т.д.).
    """

    _id_param_name: ClassVar[str] = "ID"

    def __init__(self, bitrix: Bitrix):
        """
        Инициализация миксина.

        :param bitrix: Клиент для работы с API Bitrix24
        """
        self.bitrix = bitrix

    async def add_relationship(
        self,
        method: str,
        entity_id: int,
        related_id: int,
        field_name: str = "CONTACT_ID",
        error_message: str | None = None,
    ) -> bool:
        """
        Добавление связи между сущностями.

        :param method: Метод API для добавления связи
        :param entity_id: Идентификатор основной сущности
        :param related_id: Идентификатор связанной сущности
        :param field_name: Имя поля для связи
        :param error_message: Сообщение при ошибке
        :returns: Успешность операции
        """
        if not error_message:
            error_message = (
                f"Ошибка при добавлении связи: "
                f"сущность ID={entity_id}, связь ID={related_id}"
            )

        try:
            response = await self.bitrix.call(
                method,
                {"ID": entity_id, "fields": {field_name: related_id}},
            )

            if not response or "result" not in response:
                logger.warning(f"{error_message}: получен некорректный ответ")
                return False

            return bool(response.get("result"))
        except ValueError as e:
            logger.error(f"{error_message}: некорректное значение: {e}")
            return False
        except KeyError as e:
            logger.error(f"{error_message}: отсутствует ключ: {e}")
            return False
        except AttributeError as e:
            logger.error(f"{error_message}: ошибка атрибута: {e}")
            return False
        except Exception as e:
            logger.error(f"{error_message}: {e}")
            return False

    async def remove_relationship(
        self,
        method: str,
        entity_id: int,
        related_id: int,
        field_name: str = "CONTACT_ID",
        error_message: str | None = None,
    ) -> bool:
        """
        Удаление связи между сущностями.

        :param method: Метод API для удаления связи
        :param entity_id: Идентификатор основной сущности
        :param related_id: Идентификатор связанной сущности
        :param field_name: Имя поля для связи
        :param error_message: Сообщение при ошибке
        :returns: Успешность операции
        """
        if not error_message:
            error_message = (
                f"Ошибка при удалении связи: "
                f"сущность ID={entity_id}, связь ID={related_id}"
            )

        try:
            response = await self.bitrix.call(
                method,
                {"ID": entity_id, "fields": {field_name: related_id}},
            )

            if not response or "result" not in response:
                logger.warning(f"{error_message}: получен некорректный ответ")
                return False

            return bool(response.get("result"))
        except ValueError as e:
            logger.error(f"{error_message}: некорректное значение: {e}")
            return False
        except KeyError as e:
            logger.error(f"{error_message}: отсутствует ключ: {e}")
            return False
        except AttributeError as e:
            logger.error(f"{error_message}: ошибка атрибута: {e}")
            return False
        except Exception as e:
            logger.error(f"{error_message}: {e}")
            return False

    async def get_related_items(
        self,
        method: str,
        entity_id: int,
        error_message: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Получение связанных элементов.

        :param method: Метод API для получения связанных элементов
        :param entity_id: Идентификатор основной сущности
        :param error_message: Сообщение при ошибке
        :returns: Список связанных элементов
        """
        if not error_message:
            error_message = (
                f"Ошибка при получении связанных элементов: "
                f"сущность ID={entity_id}"
            )

        try:
            response = await self.bitrix.call(
                method,
                {self._id_param_name: entity_id},
                raw=True,
            )

            if not response or "result" not in response:
                logger.warning(f"{error_message}: получен некорректный ответ")
                return []

            return response.get("result", [])
        except ValueError as e:
            logger.error(f"{error_message}: некорректное значение: {e}")
            return []
        except KeyError as e:
            logger.error(f"{error_message}: отсутствует ключ: {e}")
            return []
        except AttributeError as e:
            logger.error(f"{error_message}: ошибка атрибута: {e}")
            return []
        except Exception as e:
            logger.error(f"{error_message}: {e}")
            return []
