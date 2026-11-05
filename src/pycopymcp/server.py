"""Servidor MCP (stdio) con una única herramienta: copy_to_clipboard."""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .clipboard import ClipboardError, copy_text

mcp = FastMCP("pycopymcp")


@mcp.tool()
def copy_to_clipboard(content: str) -> str:
    """Copia el contenido de texto indicado al portapapeles del usuario.

    Úsala cuando el usuario quiera tener algo listo para pegar (código, comandos,
    texto, resultados). El contenido se copia literalmente, sin modificar.

    Args:
        content: Texto exacto a copiar al portapapeles.
    """
    if not content:
        raise ValueError("`content` no puede estar vacío")
    try:
        tool = copy_text(content)
    except ClipboardError as e:
        raise RuntimeError(str(e)) from e
    return f"Copiado al portapapeles ({len(content)} caracteres, vía {tool})."


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
