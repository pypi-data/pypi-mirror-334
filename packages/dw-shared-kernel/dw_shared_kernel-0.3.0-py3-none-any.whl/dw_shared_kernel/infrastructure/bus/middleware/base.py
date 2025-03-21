from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any


__all__ = ("BusMiddleware",)


class BusMiddleware(ABC):
    @abstractmethod
    async def __call__(self, message: Any, next_: Callable[[Any], Awaitable[Any]]) -> Any: ...
