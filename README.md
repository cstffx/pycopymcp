# pycopymcp

A tiny [MCP](https://modelcontextprotocol.io) server that does one thing: it lets an AI agent copy text to your clipboard.

## Tool

`copy_to_clipboard(content: str)` — copies the text exactly as given.

## Install

```bash
uvx --from git+https://github.com/cstffx/pycopymcp pycopymcp
```

Or with pip:

```bash
pip install git+https://github.com/cstffx/pycopymcp
```

## Use with Claude Code

```bash
claude mcp add pycopymcp -- uvx --from git+https://github.com/cstffx/pycopymcp pycopymcp
```

Generic MCP client config:

```json
{
  "mcpServers": {
    "pycopymcp": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/cstffx/pycopymcp", "pycopymcp"]
    }
  }
}
```

## Platform support

| OS | Backend | Needs |
|---|---|---|
| Windows | Win32 API (ctypes) | nothing |
| macOS | `pbcopy` | nothing |
| Linux (Wayland) | `wl-copy` | `wl-clipboard` |
| Linux (X11) | `xclip` / `xsel` | `xclip` or `xsel` |
| WSL | `clip.exe` | nothing |

On Linux the server needs access to your graphical session. If your MCP client starts it with a reduced environment, pass `WAYLAND_DISPLAY` / `DISPLAY` and `XDG_RUNTIME_DIR` in its `env`.

## Development

```bash
pip install -e ".[test]"
pytest
```

## License

[Apache License 2.0](LICENSE)
