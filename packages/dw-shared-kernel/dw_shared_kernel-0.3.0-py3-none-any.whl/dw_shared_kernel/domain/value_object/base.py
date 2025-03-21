from abc import ABC
from dataclasses import dataclass


__all__ = ("ValueObject",)


@dataclass(kw_only=True, slots=True)
class ValueObject(ABC):
    pass
