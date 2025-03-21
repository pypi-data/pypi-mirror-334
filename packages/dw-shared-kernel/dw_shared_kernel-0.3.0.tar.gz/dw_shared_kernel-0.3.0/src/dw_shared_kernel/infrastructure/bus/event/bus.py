from collections import defaultdict
from functools import cached_property
from typing import Callable, Awaitable

from dw_shared_kernel.domain.event_bus.bus import ModelEventBus
from dw_shared_kernel.domain.event_bus.event import ModelEvent
from dw_shared_kernel.infrastructure.bus.event.handler import EventHandler
from dw_shared_kernel.infrastructure.bus.mixin.middleware import MiddlewareMixin


class EventBus(ModelEventBus, MiddlewareMixin[ModelEvent, Callable[[ModelEvent], Awaitable[None]]]):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._event_handler: dict[type[ModelEvent], list[EventHandler]] = defaultdict(list)

    def register(
        self,
        event: type[ModelEvent],
        handler: EventHandler,
    ) -> None:
        self._event_handler[event].append(handler)

    async def publish(
        self,
        event: ModelEvent,
    ) -> None:
        await self._middleware_chain(event)

    @cached_property
    def _base_executor(self) -> Callable[[ModelEvent], Awaitable[None]]:
        async def event_executor(message: ModelEvent) -> None:
            for handler in self._event_handler[message.__class__]:
                await handler(
                    event=message,
                )

        return event_executor
