from dw_shared_kernel.infrastructure.bus.command.bus import CommandBus
from dw_shared_kernel.infrastructure.bus.event.bus import EventBus
from dw_shared_kernel.infrastructure.bus.event.repository import IntegrationEventRepository
from dw_shared_kernel.infrastructure.bus.query.bus import QueryBus
from dw_shared_kernel.infrastructure.di.container import Container
from dw_shared_kernel.infrastructure.di.layer import Layer


__all__ = ("SharedKernelInfrastructureLayer",)


class SharedKernelInfrastructureLayer(Layer):
    def setup(
        self,
        container: Container,
    ) -> None:
        container[QueryBus] = QueryBus()
        container[CommandBus] = CommandBus()
        container[EventBus] = EventBus()

        container[IntegrationEventRepository] = IntegrationEventRepository()
