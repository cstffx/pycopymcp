"""Copia texto al portapapeles del sistema usando herramientas nativas (sin dependencias extra)."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time


class ClipboardError(RuntimeError):
    pass


def _backends() -> list[list[str]]:
    """Comandos candidatos, en orden de preferencia según plataforma/sesión."""
    if sys.platform == "darwin":
        return [["pbcopy"]]
    if sys.platform.startswith("win"):
        return []  # se usa la API nativa (ver _copy_windows)
    # No se filtra por variables de entorno: los clientes MCP suelen lanzar el
    # servidor con un entorno reducido. Se prueba cada herramienta instalada.
    wayland = bool(os.environ.get("WAYLAND_DISPLAY"))
    wl, x11 = [["wl-copy"]], [["xclip", "-selection", "clipboard", "-in"],
                              ["xsel", "--clipboard", "--input"]]
    return (wl + x11 if wayland else x11 + wl) + [["clip.exe"]]  # clip.exe: WSL


def _copy_windows(text: str) -> None:
    """Portapapeles de Windows vía Win32 (CF_UNICODETEXT), correcto con todo Unicode."""
    import ctypes
    from ctypes import wintypes

    CF_UNICODETEXT, GMEM_MOVEABLE = 13, 0x0002
    k32, u32 = ctypes.WinDLL("kernel32", use_last_error=True), ctypes.WinDLL("user32", use_last_error=True)
    k32.GlobalAlloc.argtypes, k32.GlobalAlloc.restype = [wintypes.UINT, ctypes.c_size_t], wintypes.HGLOBAL
    k32.GlobalLock.argtypes, k32.GlobalLock.restype = [wintypes.HGLOBAL], wintypes.LPVOID
    k32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
    k32.GlobalFree.argtypes = [wintypes.HGLOBAL]
    u32.OpenClipboard.argtypes = [wintypes.HWND]
    u32.SetClipboardData.argtypes, u32.SetClipboardData.restype = [wintypes.UINT, wintypes.HANDLE], wintypes.HANDLE

    data = (text.replace("\r\n", "\n").replace("\n", "\r\n") + "\0").encode("utf-16-le")
    # El portapapeles puede estar bloqueado un instante por otro proceso: reintentar.
    for _ in range(10):
        if u32.OpenClipboard(None):
            break
        time.sleep(0.05)
    else:
        raise ClipboardError("No se pudo abrir el portapapeles de Windows (en uso por otro proceso)")
    try:
        u32.EmptyClipboard()
        handle = k32.GlobalAlloc(GMEM_MOVEABLE, len(data))
        if not handle:
            raise ClipboardError("GlobalAlloc falló")
        ptr = k32.GlobalLock(handle)
        if not ptr:
            k32.GlobalFree(handle)
            raise ClipboardError("GlobalLock falló")
        ctypes.memmove(ptr, data, len(data))
        k32.GlobalUnlock(handle)
        if not u32.SetClipboardData(CF_UNICODETEXT, handle):
            k32.GlobalFree(handle)  # si tiene éxito, la propiedad pasa al sistema
            raise ClipboardError("SetClipboardData falló")
    finally:
        u32.CloseClipboard()


def copy_text(text: str) -> str:
    """Copia `text` al portapapeles. Devuelve el nombre de la herramienta usada."""
    if sys.platform.startswith("win"):
        _copy_windows(text)
        return "win32"
    tried = []
    for cmd in _backends():
        if shutil.which(cmd[0]) is None:
            tried.append(cmd[0])
            continue
        if cmd[0] == "clip.exe":
            data = text.encode("utf-16-le")
        else:
            data = text.encode("utf-8")
        try:
            # xclip/wl-copy se quedan en segundo plano sirviendo la selección:
            # no heredar stdout/stderr para no bloquear la espera.
            proc = subprocess.run(
                cmd, input=data, stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE, timeout=5, check=False,
            )
        except subprocess.TimeoutExpired:
            # Algunos backends no terminan al hacer fork; el contenido ya se entregó.
            return cmd[0]
        if proc.returncode == 0:
            return cmd[0]
        tried.append(f"{cmd[0]} ({proc.stderr.decode(errors='replace').strip()})")
    raise ClipboardError(
        "No se pudo copiar. Instala wl-clipboard "
        "(Wayland) o xclip/xsel (X11). Probadas: " + ", ".join(tried or ["ninguna"])
    )
