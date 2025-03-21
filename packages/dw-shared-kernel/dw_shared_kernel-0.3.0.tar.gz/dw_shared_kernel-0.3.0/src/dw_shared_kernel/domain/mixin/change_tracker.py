from abc import ABC
from dataclasses import dataclass, field
from enum import auto
from typing import ClassVar

from dw_shared_kernel.utils.value_name_enum import ValueNameEnum


@dataclass(kw_only=True)
class ChangeTrackerMixin(ABC):
    _changes: dict[str, "Change"] = field(default_factory=dict)

    def flush_changes(self) -> dict[str, "Change"]:
        flushed_changes, self._changes = self._changes, {}
        return flushed_changes

    def _add_change(
        self,
        change: "Change",
    ) -> None:
        self._changes[change.name] = change

    def _has_change(
        self,
        change_name: str,
    ) -> bool:
        return change_name in self._changes


class BuiltInChangeName(ValueNameEnum):
    CREATED = auto()


@dataclass(kw_only=True, frozen=True)
class Change:
    name: ClassVar[str]


@dataclass(kw_only=True, frozen=True)
class ValueCreatedChange(Change):
    name: ClassVar[str] = BuiltInChangeName.CREATED
