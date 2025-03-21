from collections.abc import Callable, Awaitable
from functools import cached_property

from dw_shared_kernel.infrastructure.bus.command.handler import CommandHandler
from dw_shared_kernel.infrastructure.bus.command.command import Command
from dw_shared_kernel.infrastructure.bus.mixin.middleware import MiddlewareMixin


class CommandBus(MiddlewareMixin[Command, Callable[[Command], Awaitable[None]]]):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._handlers: dict[type[Command], CommandHandler] = {}

    def register(
        self,
        command: type[Command],
        handler: CommandHandler,
    ) -> None:
        self._handlers[command] = handler

    async def handle(
        self,
        command: Command,
    ) -> None:
        await self._middleware_chain(command)

    @cached_property
    def _base_executor(self) -> Callable[[Command], Awaitable[None]]:
        async def command_executor(command: Command) -> None:
            command_handler = self._handlers.get(command.__class__)

            if not command_handler:
                raise ValueError(f"Command handler doesn't exist for the '{command.__class__}' command")

            await command_handler(command=command)

        return command_executor
