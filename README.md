# LSP-html

HTML support for Sublime's LSP plugin provided through [VS Code's HTML language server](https://github.com/microsoft/vscode/tree/main/extensions/html-language-features/server) extension.

## Installation

- Install [LSP](https://packagecontrol.io/packages/LSP) and `LSP-html` from Package Control.
- Restart Sublime.

## Configuration

There are some ways to configure the package and the language server.

- From `Preferences > Package Settings > LSP > Servers > LSP-html`
- From the command palette `Preferences: LSP-html Settings`

## FAQs

- The server exited with status code 1.

  It's probably that the `node` executable on your system is outdated.
  This plugin requires v14 as of version [1.2.4](https://github.com/sublimelsp/LSP-html/releases/tag/1.2.4).
  If your OS is incapable of using Node v14 like Windows 7, you can

  - either download and use [1.2.3](https://github.com/sublimelsp/LSP-html/releases/tag/1.2.3) manually.
  - or if you want to try the hard way, you can use Node v14 on Windows 7 on your own risk.
    See https://github.com/nodejs/node/issues/33000#issuecomment-644530517.
