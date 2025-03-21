from abc import ABC

from pydantic import BaseModel


__all__ = ("Query",)


class Query(BaseModel, ABC):
    pass
