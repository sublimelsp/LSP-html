from __future__ import annotations

import os
from collections.abc import Callable

import sublime
from LSP.plugin import Session
from lsp_utils import ApiWrapperInterface, NpmClientHandler, request_handler

from .constants import PACKAGE_NAME
from .data_types import CustomDataChangedNotification, CustomDataRequest


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

    @classmethod
    def required_node_version(cls) -> str:
        return ">=14"

    @classmethod
    def should_ignore(cls, view: sublime.View) -> bool:
        return bool(
            # SublimeREPL views
            view.settings().get("repl")
            # syntax test files
            or os.path.basename(view.file_name() or "").startswith("syntax_test")
        )

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
    def on_custom_data_content_async(
        self,
        params: CustomDataRequest.Params,
        respond: Callable[[CustomDataRequest.Response], None],
    ) -> None:
        (file_path,) = params
        try:
            with open(file_path, encoding="utf-8") as fd:
                respond(fd.read())
        except Exception:
            respond("")
