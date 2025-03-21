"""
Модуль с презентационным слоем MCP сервера.

Отвечает за конфигурацию и запуск MCP сервера для Bitrix24.
"""

from mcp.server.fastmcp import FastMCP

from app.infrastructure.ioc import container
from app.infrastructure.mcp.handlers import (
    register_contact_handlers,
    register_deal_handlers,
)
from app.infrastructure.mcp.server import BitrixMCPServer


@container.autowire
def create_mcp_server(mcp_server: BitrixMCPServer) -> FastMCP:
    """
    Создание и настройка MCP сервера для Bitrix24.

    Регистрирует все обработчики, промпты и инструменты.

    :return: Настроенный экземпляр MCP сервера
    """
    mcp_server.add_prompt(
        lambda: (
            "Я - ассистент Bitrix24, специализирующийся на работе с CRM-системой. "
            "Я могу помочь вам найти информацию о контактах, "
            "сделках и других сущностях Bitrix24. "
            "Как я могу вам помочь сегодня?"
        ),
        name="bitrix24_assistant",
        description="Подсказка для ассистента Bitrix24",
    )

    mcp_server.add_prompt(
        lambda query: f"Выполните поиск контактов по запросу: {query}",
        name="search_contacts_prompt",
        description="Подсказка для поиска контактов",
    )

    mcp_server.add_prompt(
        lambda query: f"Найдите активные сделки, соответствующие запросу: {query}",
        name="search_deals_prompt",
        description="Подсказка для поиска сделок",
    )

    register_contact_handlers(mcp_server)
    register_deal_handlers(mcp_server)

    return mcp_server.server


server = create_mcp_server()


def main():
    server.run()
