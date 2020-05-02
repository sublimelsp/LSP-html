import os
from lsp_utils import NpmClientHandler


def plugin_loaded():
    LspHtmlPlugin.setup()


def plugin_unloaded():
    LspHtmlPlugin.cleanup()


class LspHtmlPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'vscode-html'
    server_binary_path = os.path.join(server_directory, 'out', 'htmlServerMain.js')
