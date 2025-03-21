"""
Модуль с контейнером зависимостей приложения.

Предоставляет единую точку инициализации и получения зависимостей.
"""

from wireup import create_container

from app import application
from app.config import settings

from .bitrix import repository_factory
from .mcp import server

container = create_container(
    parameters={"bitrix_webhook_url": settings.BITRIX_WEBHOOK_URL},
    service_modules=[server, repository_factory, application],
)
