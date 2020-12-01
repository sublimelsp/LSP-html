import os
from lsp_utils import NpmClientHandler
import sublime


def plugin_loaded():
    LspHtmlPlugin.setup()


def plugin_unloaded():
    LspHtmlPlugin.cleanup()


class LspHtmlPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'language-server'
    server_binary_path = os.path.join(server_directory, 'out', 'node', 'htmlServerMain.js')

    @classmethod
    def install_in_cache(cls) -> bool:
        return False

    def on_pre_server_command(self, command, done_callback):
        cmd = command["command"]
        if cmd == "editor.action.triggerSuggest":
            session = self.weaksession()
            if session:
                view = session.window.active_view()
                if view:
                    sublime.set_timeout(lambda: view.run_command("auto_complete"))
                    done_callback()
                    return True
        return False
