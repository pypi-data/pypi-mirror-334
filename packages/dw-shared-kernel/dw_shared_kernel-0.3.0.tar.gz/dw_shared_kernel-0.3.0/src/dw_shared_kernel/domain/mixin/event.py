from abc import ABC
from dataclasses import dataclass, field

from dw_shared_kernel.domain.event_bus.event import ModelEvent


@dataclass(kw_only=True)
class EventMixin(ABC):
    _events: list[ModelEvent] = field(default_factory=list)

    def flush_events(self) -> list[ModelEvent]:
        flushed_events, self._events = self._events, []
        return flushed_events

    def _add_event(
        self,
        event: ModelEvent,
    ) -> None:
        self._events.append(event)
