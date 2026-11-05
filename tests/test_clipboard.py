import sys

import pytest

from pycopymcp.clipboard import ClipboardError, copy_text


def norm(s: str) -> str:
    return s.replace("\r\n", "\n").rstrip("\n")


@pytest.mark.parametrize("text", [
    "hola mundo",
    "acentos ñ á ü € 日本語",
    "emoji 😀 🚀",
    "línea1\nlínea2\n\ttabulada",
    "x" * 100_000,
])
def test_roundtrip(paste, text):
    copy_text(text)
    assert norm(paste()) == norm(text)


def test_overwrites_previous(paste):
    copy_text("primero")
    copy_text("segundo")
    assert norm(paste()) == "segundo"


@pytest.mark.skipif(sys.platform.startswith("win"), reason="usa binarios externos")
def test_error_without_backend(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: None)
    with pytest.raises(ClipboardError):
        copy_text("x")
