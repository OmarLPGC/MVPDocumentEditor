from pathlib import Path

import pytest

from editor.io import DocumentIOError, load_document, save_document
from editor.model import Document, TextStyle


def test_save_and_load_preserves_text_and_format(tmp_path: Path) -> None:
    document = Document("Documento guardado")
    document.insert_text("Hola", style=TextStyle(bold=True))
    document.add_paragraph("Segunda línea", alignment="center")
    path = tmp_path / "document.html"

    save_document(document, path)
    loaded = load_document(path)

    assert loaded.title == "Documento guardado"
    assert loaded.content == "Hola\nSegunda línea"
    assert loaded.paragraphs[0].runs[0].style.bold is True
    assert loaded.paragraphs[1].alignment == "center"


def test_save_writes_utf8_html(tmp_path: Path) -> None:
    path = tmp_path / "unicode.html"
    save_document(Document("Título ñ €"), path)

    assert "Título ñ €" in path.read_text(encoding="utf-8")


def test_load_rejects_malicious_html(tmp_path: Path) -> None:
    path = tmp_path / "unsafe.html"
    path.write_text("<script>alert(1)</script>", encoding="utf-8")

    with pytest.raises(DocumentIOError):
        load_document(path)


def test_load_failure_does_not_mutate_existing_document(tmp_path: Path) -> None:
    current = Document("Actual")
    current.insert_text("Contenido actual")
    path = tmp_path / "unsafe.html"
    path.write_text('<p onclick="alert(1)">malicioso</p>', encoding="utf-8")

    with pytest.raises(DocumentIOError):
        load_document(path)

    assert current.title == "Actual"
    assert current.content == "Contenido actual"


def test_save_rejects_non_html_extension(tmp_path: Path) -> None:
    with pytest.raises(DocumentIOError, match="extension"):
        save_document(Document(), tmp_path / "document.txt")
