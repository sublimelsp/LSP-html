from lsp_utils import NpmClientHandler
import os


def plugin_loaded():
    LspHtmlPlugin.setup()


def plugin_unloaded():
    LspHtmlPlugin.cleanup()


class LspHtmlPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = "language-server"
    server_binary_path = os.path.join(
        server_directory,
        "extensions",
        "html-language-features",
        "out",
        "node",
        "htmlServerMain.js",
    )
