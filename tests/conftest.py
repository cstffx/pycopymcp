import shutil
import subprocess
import sys

import pytest


def read_clipboard() -> str | None:
    """Lee el portapapeles con una herramienta independiente de la implementación."""
    if sys.platform == "darwin":
        cmd = ["pbpaste"]
    elif sys.platform.startswith("win"):
        cmd = ["powershell", "-NoProfile", "-Command",
               "[Console]::OutputEncoding=[Text.Encoding]::UTF8; Get-Clipboard -Raw"]
    elif shutil.which("xclip"):
        cmd = ["xclip", "-selection", "clipboard", "-out"]
    elif shutil.which("wl-paste"):
        cmd = ["wl-paste", "--no-newline"]
    else:
        return None
    out = subprocess.run(cmd, capture_output=True, timeout=15, check=True).stdout
    return out.decode("utf-8")


@pytest.fixture
def paste():
    try:
        probe = read_clipboard()
    except Exception as e:  # sin portapapeles utilizable en este entorno
        pytest.skip(f"portapapeles no disponible: {e}")
    if probe is None:
        pytest.skip("no hay herramienta para leer el portapapeles")
    return read_clipboard
