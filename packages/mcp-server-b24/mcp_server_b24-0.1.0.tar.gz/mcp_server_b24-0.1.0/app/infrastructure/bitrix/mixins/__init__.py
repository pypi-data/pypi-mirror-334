"""
Пакет с миксинами для работы с API Bitrix24.

Миксины предоставляют функциональность для различных аспектов
взаимодействия с API Bitrix24.
"""

from app.infrastructure.bitrix.mixins.batch_operations import (
    BitrixBatchOperationsMixin,
)
from app.infrastructure.bitrix.mixins.error_handling import (
    BitrixErrorHandlingMixin,
)
from app.infrastructure.bitrix.mixins.filter_builder import (
    BitrixFilterBuilderMixin,
)
from app.infrastructure.bitrix.mixins.pagination import BitrixPaginationMixin
from app.infrastructure.bitrix.mixins.read import BitrixReadMixin
from app.infrastructure.bitrix.mixins.relationship import (
    BitrixRelationshipMixin,
)
from app.infrastructure.bitrix.mixins.write import BitrixWriteMixin

__all__ = [
    "BitrixBatchOperationsMixin",
    "BitrixErrorHandlingMixin",
    "BitrixFilterBuilderMixin",
    "BitrixPaginationMixin",
    "BitrixReadMixin",
    "BitrixRelationshipMixin",
    "BitrixWriteMixin",
]
