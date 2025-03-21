from dw_shared_kernel.domain.event_bus.event import IntegrationEvent
from dw_shared_kernel.infrastructure.message_broker.destination import MessageDestination


class IntegrationEventRepository:
    def __init__(self):
        self._mapper: dict[type[IntegrationEvent], MessageDestination] = {}
        self._events = []

    def add_event_destination(
        self,
        event: type[IntegrationEvent],
        destination: MessageDestination,
    ) -> None:
        self._mapper[event] = destination

    def add_event(
        self,
        event: type[IntegrationEvent],
    ) -> None:
        if self.get_event_by_name(event.__event_name__):
            raise ValueError(f"Event with name {event.__event_name__} already exists")
        self._events.append(event)

    def get_event_by_name(
        self,
        name: str,
    ) -> IntegrationEvent | None:
        return next(filter(lambda e: e.__event_name__ == name, self._events), None)

    def get_event_destination(
        self,
        event: type[IntegrationEvent],
    ) -> MessageDestination | None:
        return self._mapper.get(event)
