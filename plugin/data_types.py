from __future__ import annotations

from typing import List, Tuple

from LSP.plugin import Notification
from typing_extensions import TypeAlias

FilePath: TypeAlias = str


class CustomDataChangedNotification:
    Type = "html/customDataChanged"
    Params: TypeAlias = List[FilePath]

    @classmethod
    def create(cls, params: Params) -> Notification:
        return Notification(cls.Type, [params])


class CustomDataRequest:
    Type = "html/customDataContent"
    Params: TypeAlias = Tuple[FilePath]
    Response: TypeAlias = str
