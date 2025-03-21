from abc import ABC, abstractmethod
from functools import cached_property

from dw_shared_kernel.infrastructure.bus.middleware.base import BusMiddleware


class MiddlewareMixin[MESSAGE, HANDLER](ABC):
    def __init__(
        self,
        *args,
        middlewares: list[BusMiddleware] | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._middlewares = middlewares or []

    def add_middlewares(
        self,
        middlewares: list[BusMiddleware],
    ) -> None:
        self._middlewares = middlewares + self._middlewares
        self._middleware_chain = self._build_middleware_chain()

    def _build_middleware_chain(self) -> HANDLER:
        command_executor = self._base_executor

        def wrapped_middleware(
            middleware: BusMiddleware,
            next_handler: HANDLER,
        ) -> HANDLER:
            async def wrapped_handler(command: MESSAGE) -> None:
                return await middleware(
                    message=command,
                    next_=next_handler,  # type: ignore
                )

            return wrapped_handler  # type: ignore

        for mdl in self._middlewares[::-1]:
            command_executor = wrapped_middleware(  # type: ignore
                middleware=mdl,
                next_handler=command_executor,
            )

        return command_executor

    @cached_property
    @abstractmethod
    def _base_executor(self) -> HANDLER: ...
