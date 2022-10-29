from .types import CustomDataChangedNotification, CustomDataRequest
from LSP.plugin import Session
from LSP.plugin.core.typing import Callable, List
from lsp_utils import ApiWrapperInterface, NpmClientHandler, request_handler
from os import path


def plugin_loaded():
    LspHtmlPlugin.setup()


def plugin_unloaded():
    LspHtmlPlugin.cleanup()


class LspHtmlPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = "language-server"
    server_binary_path = path.join(
        server_directory,
        "html-language-features",
        "server",
        "out",
        "node",
        "htmlServerMain.js",
    )

    @classmethod
    def required_node_version(cls) -> str:
        return '>=14'

    def on_ready(self, api: ApiWrapperInterface) -> None:
        session = self.weaksession()
        if not session:
            return
        self.resolve_custom_data_paths(session)

    def resolve_custom_data_paths(self, session: Session) -> None:
        custom_data_paths = session.config.settings.get('html.customData')  # type: List[str]
        resolved_custom_data_paths = []  # type: List[str]
        for folder in session.get_workspace_folders():
            resolved_custom_data_paths.extend([path.abspath(path.join(folder.path, p)) for p in custom_data_paths])
        session.send_notification(CustomDataChangedNotification.create(resolved_custom_data_paths))

    @request_handler(CustomDataRequest.Type)
    def on_custom_data_content_async(
        self, params: CustomDataRequest.Params, respond: Callable[[CustomDataRequest.Response], None]
    ) -> None:
        file_path, = params
        if path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as fd:
                respond(fd.read())
                return
        respond('')
