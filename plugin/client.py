from __future__ import annotations

from pathlib import Path
from typing import final

from LSP.plugin import LspPlugin, OnPreStartContext, Promise, Session, request_handler
from lsp_utils import NodeManager
from sublime_lib import ResourcePath
from typing_extensions import override

from .data_types import CustomDataChangedNotification, CustomDataRequest


@final
class LspHtmlPlugin(LspPlugin):
    @classmethod
    @override
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        package_name = cls.plugin_storage_path.name
        NodeManager.on_pre_start_async(
            context,
            cls.plugin_storage_path,
            ResourcePath("Packages", package_name, "language-server"),
            Path("html-language-features", "server", "out", "node", "htmlServerNodeMain.js"),
            node_version_requirement=">=14",
        )

    @override
    def on_initialized_async(self) -> None:
        if session := self.weaksession():
            self.resolve_custom_data_paths(session)

    def resolve_custom_data_paths(self, session: Session) -> None:
        custom_data_paths: list[str] = session.config.settings.get("html.customData")
        resolved_custom_data_paths: list[str] = []
        for folder in session.get_workspace_folders():
            resolved_custom_data_paths.extend(str(Path(folder.path, p).absolute()) for p in custom_data_paths)
        session.send_notification(CustomDataChangedNotification.create(resolved_custom_data_paths))

    @request_handler(CustomDataRequest.Type)
    def on_custom_data_content_async(self, params: CustomDataRequest.Params) -> Promise[CustomDataRequest.Response]:
        (file_path,) = params
        try:
            with open(file_path, encoding="utf-8") as fd:
                return Promise.resolve(fd.read())
        except Exception:
            return Promise.resolve("")
