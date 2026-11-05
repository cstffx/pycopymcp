# pycopymcp

Servidor MCP (stdio) con una única herramienta: `copy_to_clipboard(content)`, que
copia el texto literal al portapapeles del sistema.

## Soporte por plataforma
| SO | Mecanismo | Requiere instalar |
|---|---|---|
| Windows | API Win32 nativa (CF_UNICODETEXT, vía ctypes) | nada |
| macOS | `pbcopy` | nada |
| Linux Wayland | `wl-copy` | `wl-clipboard` |
| Linux X11 | `xclip` / `xsel` | `xclip` o `xsel` |
| WSL | `clip.exe` (último recurso) | nada |

## Instalación y ejecución (sin rutas fijas)
Con [uv](https://docs.astral.sh/uv/) (recomendado, no hace falta instalar nada antes):

    uvx pycopymcp                                   # si está publicado en PyPI
    uvx --from /ruta/al/repo pycopymcp              # desde una copia local
    uvx --from git+https://<tu-repo>.git pycopymcp  # desde git

Con pipx:

    pipx install /ruta/al/repo      # o: pipx install pycopymcp
    pycopymcp

Con pip clásico: `pip install .` y `python -m pycopymcp`.

## Configuración del cliente
Claude Code:

    claude mcp add pycopymcp -- uvx pycopymcp

JSON genérico:

    {"mcpServers": {"pycopymcp": {"command": "uvx", "args": ["pycopymcp"]}}}

En Linux el servidor necesita acceso a la sesión gráfica: si el cliente lanza el
proceso con entorno reducido, añade `WAYLAND_DISPLAY` / `DISPLAY` (y `XDG_RUNTIME_DIR`) en `env`.

## Tests y CI
    pip install -e ".[test]" && pytest

El workflow `.github/workflows/ci.yml` ejecuta los tests en Ubuntu (xvfb + xclip), macOS y Windows, con Python 3.10 y 3.13, y construye el paquete.

## Publicar
    uv build && uv publish      # o: python -m build && twine upload dist/*
