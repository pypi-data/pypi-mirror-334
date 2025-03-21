from typing import Any

from dw_shared_kernel.infrastructure.bus.query.handler import QueryHandler
from dw_shared_kernel.infrastructure.bus.query.query import Query


__all__ = ("QueryBus",)


class QueryBus:
    def __init__(self):
        self._handlers = {}

    def register(
        self,
        query: type[Query],
        handler: QueryHandler,
    ) -> None:
        self._handlers[query] = handler

    async def handle(
        self,
        query: Query,
    ) -> Any:
        query_handler = self._handlers.get(query.__class__)

        if not query_handler:
            raise ValueError(f"Query handler doesn't exist for the '{query.__class__}' query")

        return await query_handler(query)
