from LSP.plugin import Notification
from LSP.plugin.core.typing import List, Tuple


FilePath = str


class CustomDataChangedNotification:
    Type = 'html/customDataChanged'
    Params = List[FilePath]

    @classmethod
    def create(cls, params: Params) -> Notification:
        return Notification(cls.Type, [params])


class CustomDataRequest:
    Type = 'html/customDataContent'
    Params = Tuple[FilePath]
    Response = str
