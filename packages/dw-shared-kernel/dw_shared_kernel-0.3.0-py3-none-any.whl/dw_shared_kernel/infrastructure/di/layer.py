from abc import ABC, abstractmethod

from dw_shared_kernel.infrastructure.di.container import Container


__all__ = ("Layer",)


class Layer(ABC):
    @abstractmethod
    def setup(self, container: Container) -> None: ...
