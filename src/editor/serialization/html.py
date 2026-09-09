"""Deterministic, safe HTML serialization for the internal document model."""

from __future__ import annotations

from html import escape
import math
import re

from editor.model import Document, TextStyle

_SAFE_FONT_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _-]{0,79}$")
_ALIGNMENT_VALUES = frozenset({"left", "center", "right", "justify"})


def serialize_document(document: Document) -> str:
    """Serialize a document to UTF-8-compatible HTML with inline styles only."""

    title = escape(document.title, quote=True)
    paragraphs = "\n".join(_serialize_paragraph(paragraph) for paragraph in document.paragraphs)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="es">\n'
        "<head>\n"
        f"<title>{title}</title>\n"
        "</head>\n"
        "<body>\n"
        f"{paragraphs}\n"
        "</body>\n"
        "</html>\n"
    )


def _serialize_paragraph(paragraph: object) -> str:
    alignment = getattr(paragraph, "alignment", "left")
    if alignment not in _ALIGNMENT_VALUES:
        alignment = "left"
    runs = getattr(paragraph, "runs", [])
    content = "".join(_serialize_run(run.text, run.style) for run in runs)
    return f'<p style="text-align:{alignment}">{content}</p>'


def _serialize_run(text: str, style: TextStyle) -> str:
    styles: list[str] = []
    if style.bold:
        styles.append("font-weight:bold")
    if style.italic:
        styles.append("font-style:italic")
    if style.underline:
        styles.append("text-decoration:underline")

    if style.font_family and _SAFE_FONT_NAME.fullmatch(style.font_family):
        styles.append(f"font-family:{escape(style.font_family, quote=True)}")
    if (
        style.font_size is not None
        and math.isfinite(style.font_size)
        and 0 < style.font_size <= 1000
    ):
        styles.append(f"font-size:{style.font_size:g}pt")

    escaped_text = escape(text, quote=False)
    if not styles:
        return escaped_text
    return f'<span style="{";".join(styles)}">{escaped_text}</span>'
