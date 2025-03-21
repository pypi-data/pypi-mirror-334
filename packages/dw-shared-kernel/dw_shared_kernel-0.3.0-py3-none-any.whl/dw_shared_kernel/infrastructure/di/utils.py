from collections.abc import Iterable

from dw_shared_kernel.infrastructure.di.container import Container
from dw_shared_kernel.infrastructure.di.layer import Layer


__all__ = ("get_di_container",)


def get_di_container(
    layers: Iterable[Layer],
) -> Container:
    container = Container()

    for layer in layers:
        layer.setup(
            container=container,
        )

    return container
