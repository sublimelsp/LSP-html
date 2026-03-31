from __future__ import annotations

from LSP.plugin import Notification
from typing import List
from typing import Tuple
from typing_extensions import TypeAlias

FilePath: TypeAlias = str


class CustomDataChangedNotification:
    Type = "html/customDataChanged"
    Params: TypeAlias = List[FilePath]

    @classmethod
    def create(cls, params: Params) -> Notification[list[Params]]:
        return Notification(cls.Type, [params])


class CustomDataRequest:
    Type = "html/customDataContent"
    Params: TypeAlias = Tuple[FilePath]
    Response: TypeAlias = str
