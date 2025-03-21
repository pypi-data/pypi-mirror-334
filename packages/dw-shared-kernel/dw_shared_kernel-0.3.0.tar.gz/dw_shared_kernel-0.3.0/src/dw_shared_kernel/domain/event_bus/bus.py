from abc import ABC, abstractmethod

from dw_shared_kernel.domain.event_bus.event import ModelEvent
from dw_shared_kernel.infrastructure.bus.event.handler import EventHandler


class ModelEventBus(ABC):
    @abstractmethod
    async def publish(self, event: ModelEvent) -> None: ...

    @abstractmethod
    def register[EVENT: ModelEvent](self, event: type[EVENT], handler: EventHandler[EVENT]) -> None: ...
