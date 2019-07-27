import shutil
import os
import sublime

from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import ClientConfig, LanguageConfig

package_path = os.path.dirname(__file__)
server_path = os.path.join(package_path, 'node_modules', 'vscode-html-languageserver-bin', 'htmlServerMain.js')


def plugin_loaded():
    print('LSP-html: Server {} installed.'.format('is' if os.path.isfile(server_path) else 'is not' ))

    if not os.path.isdir(os.path.join(package_path, 'node_modules')):
        # install server if no node_modules
        print('LSP-html: Installing server.')
        sublime.active_window().run_command(
            "exec", {
                "cmd": [
                    "npm",
                    "install",
                    "--verbose",
                    "--prefix",
                    package_path
                ]
            }
        )
        sublime.message_dialog('LSP-html\n\nRestart sublime after the server has been installed successfully.')


def is_node_installed():
    return shutil.which('node') is not None


def is_installed(dependency):
    return shutil.which(dependency) is not None


class LspHtmlPlugin(LanguageHandler):
    @property
    def name(self) -> str:
        return 'lsp-html'

    @property
    def config(self) -> ClientConfig:
        return ClientConfig(
            name='lsp-html',
            binary_args=[
                "html-languageserver",
                "--stdio"
            ],
            tcp_port=None,
            enabled=True,
            init_options=dict(),
            settings=dict(),
            env=dict(),
            languages=[
                LanguageConfig(
                    'html',
                    ['text.html.basic'],
                    [
                        "Packages/HTML/HTML.sublime-syntax",
                        "Packages/PHP/PHP.sublime-syntax"
                    ]
                )
            ]
        )

    def on_start(self, window) -> bool:
        if not is_node_installed():
            sublime.status_message('Please install Node.js for the HTML Language Server to work.')
            return False
        return True

    def on_initialized(self, client) -> None:
        pass   # extra initialization here.
