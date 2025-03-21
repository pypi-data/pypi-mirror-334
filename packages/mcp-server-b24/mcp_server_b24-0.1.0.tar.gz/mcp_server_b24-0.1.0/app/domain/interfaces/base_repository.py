"""
Модуль с базовыми интерфейсами репозиториев.
Содержит абстрактные классы для работы с различными сущностями Bitrix24.
"""

from abc import ABC, abstractmethod
from typing import ClassVar

from app.domain.entities.base_entity import BitrixEntity


class BitrixRepository[T: BitrixEntity](ABC):
    """
    Базовый интерфейс репозитория для работы с сущностями Bitrix24.
    Определяет общие методы для всех репозиториев, работающих с сущностями Bitrix24.
    """

    _entity_type: ClassVar[str]

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> T | None:
        """
        Получение сущности по её идентификатору.

        :param entity_id: Идентификатор сущности
        :return: Объект сущности или None, если сущность не найдена
        """

    @abstractmethod
    async def list_entities(
        self,
        filter_params: dict | None = None,
        select_fields: list[str] | None = None,
        order: dict | None = None,
        start: int = 0,
        limit: int = 50,
    ) -> list[T]:
        """
        Получение списка сущностей с возможностью фильтрации.

        :param filter_params: Параметры фильтрации сущностей
        :param select_fields: Список полей для выбора
        :param order: Параметры сортировки
        :param start: Начальная позиция выборки
        :param limit: Максимальное количество возвращаемых сущностей
        :return: Список объектов сущностей
        """

    @abstractmethod
    async def get_fields(self) -> dict:
        """
        Получение описания полей сущности.

        :return: Словарь с описанием полей сущности
        """

    def supports_entity_type(self, entity_type: str) -> bool:
        """
        Проверяет, поддерживает ли репозиторий указанный тип сущности.

        :param entity_type: Тип сущности для проверки
        :return: True, если репозиторий поддерживает указанный тип сущности, иначе False
        """
        return entity_type == self._entity_type
