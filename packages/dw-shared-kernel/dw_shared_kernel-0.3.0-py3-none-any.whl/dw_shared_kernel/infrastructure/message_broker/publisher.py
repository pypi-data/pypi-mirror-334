from abc import ABC, abstractmethod

from dw_shared_kernel.infrastructure.message_broker.destination import MessageDestination


class MessageBrokerPublisher[DESTINATION: MessageDestination](ABC):
    @abstractmethod
    async def publish(self, message: bytes, destination: DESTINATION) -> None: ...
