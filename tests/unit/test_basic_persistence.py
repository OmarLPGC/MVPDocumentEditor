from pathlib import Path


def test_utf8_text_can_be_written_and_read(tmp_path: Path) -> None:
    document_path = tmp_path / "document.html"
    content = "<p>Texto Unicode: áéíóú ñ € ✓</p>"

    document_path.write_text(content, encoding="utf-8")

    assert document_path.read_text(encoding="utf-8") == content


def test_missing_document_is_not_read_as_empty_content(tmp_path: Path) -> None:
    document_path = tmp_path / "missing.html"

    assert not document_path.exists()
