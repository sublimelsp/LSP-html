from __future__ import annotations

from .constants import PACKAGE_NAME
from .data_types import CustomDataChangedNotification
from .data_types import CustomDataRequest
from LSP.plugin import ClientConfig
from LSP.plugin import Promise
from LSP.plugin import request_handler
from LSP.plugin import Session
from lsp_utils import ApiWrapperInterface
from lsp_utils import NpmClientHandler
from typing import final
from typing_extensions import override
import os
import sublime


@final
class LspHtmlPlugin(NpmClientHandler):
    package_name = PACKAGE_NAME
    server_directory = "language-server"
    server_binary_path = os.path.join(
        server_directory,
        "html-language-features",
        "server",
        "out",
        "node",
        "htmlServerNodeMain.js",
    )

    @override
    @classmethod
    def required_node_version(cls) -> str:
        return ">=14"

    @override
    @classmethod
    def is_applicable(cls, view: sublime.View, config: ClientConfig) -> bool:
        return bool(
            super().is_applicable(view, config)
            # REPL views (https://github.com/sublimelsp/LSP-pyright/issues/343)
            and not view.settings().get("repl")
        )

    @override
    def on_ready(self, api: ApiWrapperInterface) -> None:
        session = self.weaksession()
        if not session:
            return
        self.resolve_custom_data_paths(session)

    def resolve_custom_data_paths(self, session: Session) -> None:
        custom_data_paths: list[str] = session.config.settings.get("html.customData")
        resolved_custom_data_paths: list[str] = []
        for folder in session.get_workspace_folders():
            resolved_custom_data_paths.extend(os.path.abspath(os.path.join(folder.path, p)) for p in custom_data_paths)
        session.send_notification(CustomDataChangedNotification.create(resolved_custom_data_paths))

    @request_handler(CustomDataRequest.Type)
    def on_custom_data_content_async(self, params: CustomDataRequest.Params) -> Promise[CustomDataRequest.Response]:
        (file_path,) = params
        try:
            with open(file_path, encoding="utf-8") as fd:
                return Promise.resolve(fd.read())
        except Exception:
            return Promise.resolve("")
