"""
Модуль с фабрикой репозиториев Bitrix.
Предоставляет единую точку доступа к экземплярам репозиториев.
"""

from typing import Annotated

from fast_bitrix24 import Bitrix
from wireup import Inject, service

from app.domain.interfaces.base_repository import BitrixRepository
from app.infrastructure.bitrix.bitrix_contact_repository import (
    BitrixContactRepository,
)
from app.infrastructure.bitrix.bitrix_deal_repository import (
    BitrixDealRepository,
)
from app.infrastructure.logging.logger import logger


class BitrixRepositoryFactory:
    """
    Фабрика для получения репозиториев Bitrix.
    Предоставляет централизованное управление доступом к репозиториям по типу сущности.
    Выступает в роли реестра репозиториев и обеспечивает их поиск по
    соответствующему типу сущности.
    """

    def __init__(
        self,
        repository_classes: list[BitrixRepository],
    ):
        """
        Инициализация фабрики репозиториев.

        :param bitrix_client: Клиент Bitrix для работы с API
        :param repository_classes: Список уже созданных экземпляров
        репозиториев для регистрации
        """
        self._repository_classes = repository_classes

    def get_repository(self, entity_type: str) -> BitrixRepository:
        """
        Получение репозитория по типу сущности.

        :param entity_type: Тип сущности (например, 'contact', 'deal', 'smart_process')
        :return: Соответствующий репозиторий
        :raises ValueError: Если указан неизвестный тип сущности
        """
        entity_type = entity_type.lower()
        for repository in self._repository_classes:
            if repository.supports_entity_type(entity_type):
                return repository
        raise ValueError(f"Неизвестный тип сущности: {entity_type}")


@service
def provide_repository_factory(
    bitrix_webhook_url: Annotated[str, Inject(param="bitrix_webhook_url")],
) -> BitrixRepositoryFactory:
    """
    Создание фабрики репозиториев Bitrix24.

    :param bitrix_client: Клиент Bitrix24
    :return: Экземпляр фабрики репозиториев
    """
    bitrix_client = Bitrix(bitrix_webhook_url)
    logger.info("Инициализация фабрики репозиториев Bitrix24")
    contact_repository = BitrixContactRepository(bitrix_client)
    return BitrixRepositoryFactory(
        [
            contact_repository,
            BitrixDealRepository(bitrix_client, contact_repository),
        ],
    )
