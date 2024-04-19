from __future__ import annotations

import os
from collections.abc import Callable

from LSP.plugin import Session, filename_to_uri
from lsp_utils import ApiWrapperInterface, NpmClientHandler, request_handler

from .data_types import CustomDataChangedNotification, CustomDataRequest

assert __package__


def plugin_loaded() -> None:
    LspHtmlPlugin.setup()


def plugin_unloaded() -> None:
    LspHtmlPlugin.cleanup()


class LspHtmlPlugin(NpmClientHandler):
    package_name = __package__
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

    def on_ready(self, api: ApiWrapperInterface) -> None:
        session = self.weaksession()
        if not session:
            return
        self.resolve_custom_data_paths(session)

    def resolve_custom_data_paths(self, session: Session) -> None:
        custom_data_paths: list[str] = session.config.settings.get("html.customData")
        resolved_custom_data_paths: list[str] = []
        for folder in session.get_workspace_folders():
            resolved_custom_data_paths.extend(
                filename_to_uri(os.path.abspath(os.path.join(folder.path, p))) for p in custom_data_paths
            )
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
