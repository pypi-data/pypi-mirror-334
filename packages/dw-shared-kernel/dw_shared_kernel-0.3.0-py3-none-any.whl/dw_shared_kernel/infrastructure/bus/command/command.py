from abc import ABC

from pydantic import BaseModel


__all__ = ("Command",)


class Command(BaseModel, ABC):
    pass
