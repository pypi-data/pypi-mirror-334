from abc import ABC, abstractmethod

from dw_shared_kernel.domain.event_bus.event import ModelEvent


class EventHandler[EVENT: ModelEvent](ABC):
    @abstractmethod
    async def __call__(self, event: EVENT) -> None: ...
