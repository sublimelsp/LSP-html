from __future__ import annotations

from typing import List, Tuple

from LSP.plugin import Notification

FilePath = str


class CustomDataChangedNotification:
    Type = "html/customDataChanged"
    Params = List[FilePath]

    @classmethod
    def create(cls, params: Params) -> Notification:
        return Notification(cls.Type, [params])


class CustomDataRequest:
    Type = "html/customDataContent"
    Params = Tuple[FilePath]
    Response = str
