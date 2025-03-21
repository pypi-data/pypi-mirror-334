from abc import ABC

from pydantic import BaseModel


class MessageDestination(BaseModel, ABC):
    pass
