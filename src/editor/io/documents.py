"""Document file persistence built on safe validation and HTML serialization."""

from __future__ import annotations

from pathlib import Path

from editor.model import Document
from editor.serialization import deserialize_document, serialize_document
from editor.validation import validate_file


class DocumentIOError(ValueError):
    """Raised when a document cannot be saved or loaded safely."""


def save_document(document: Document, path: str | Path) -> None:
    """Write a document as UTF-8 HTML."""

    destination = Path(path)
    if destination.suffix.casefold() not in {".html", ".htm"}:
        raise DocumentIOError("Documents must use an .html or .htm extension")
    try:
        destination.write_text(serialize_document(document), encoding="utf-8")
    except OSError as exc:
        raise DocumentIOError(f"Unable to save document: {destination}") from exc


def load_document(path: str | Path) -> Document:
    """Validate and load a safe HTML document without mutating current state."""

    source = Path(path)
    try:
        validate_file(source)
        content = source.read_text(encoding="utf-8")
        return deserialize_document(content)
    except (OSError, UnicodeError, ValueError) as exc:
        if isinstance(exc, DocumentIOError):
            raise
        raise DocumentIOError(f"Unable to open document: {source}") from exc
