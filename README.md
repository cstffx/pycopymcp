# pycopymcp

[![CI](https://github.com/cstffx/pycopymcp/actions/workflows/ci.yml/badge.svg)](https://github.com/cstffx/pycopymcp/actions/workflows/ci.yml)
[![M8ven Score](https://m8ven.ai/badge/mcp/cstffx-pycopymcp-1ggyxv?v=034d4f3da9b2ed2335ce8b93110d9fa2)](https://m8ven.ai/mcp/cstffx-pycopymcp-1ggyxv?s=readme)

Let an AI agent copy text straight to your clipboard.

## Features

- **Single tool**: `copy_to_clipboard(content)` copies the text exactly as given
- **Cross-platform**: Windows (Win32), macOS (`pbcopy`), Linux (`wl-copy`, `xclip`, `xsel`) and WSL
- **MCP server**: Model Context Protocol over stdio, works with any MCP client
- **Zero setup**: Run it with `uvx`, no clone needed

## Usage

```bash
claude mcp add pycopymcp -- uvx --from git+https://github.com/cstffx/pycopymcp pycopymcp
```

On Linux, install `wl-clipboard` (Wayland) or `xclip` (X11).

## License

[Apache License 2.0](LICENSE)
