"""Deterministic, safe HTML serialization for the internal document model."""

from __future__ import annotations

from html import escape
from html.parser import HTMLParser
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


class _DocumentParser(HTMLParser):
    """Parse the restricted HTML emitted by ``serialize_document``."""

    _ALLOWED_TAGS = frozenset({"html", "head", "title", "body", "p", "span", "br"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.paragraphs: list[tuple[str, list[tuple[str, TextStyle]]]] = []
        self._current: tuple[str, list[tuple[str, TextStyle]]] | None = None
        self._style_stack = [TextStyle()]
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in self._ALLOWED_TAGS:
            raise ValueError(f"Unsupported HTML element: <{tag}>")
        attributes = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "p":
            alignment = _alignment_from_style(attributes.get("style", ""))
            self._current = (alignment, [])
        elif tag == "span":
            self._style_stack.append(
                _style_from_inline_css(attributes.get("style", ""))
            )
        elif tag == "br" and self._current is not None:
            self._current[1].append(("\n", self._style_stack[-1]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "p" and self._current is not None:
            self.paragraphs.append(self._current)
            self._current = None
        elif tag == "span" and len(self._style_stack) > 1:
            self._style_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        elif self._current is not None and data:
            self._current[1].append((data, self._style_stack[-1]))


def deserialize_document(html_text: str) -> Document:
    """Deserialize restricted safe HTML into the internal document model."""

    parser = _DocumentParser()
    parser.feed(html_text)
    parser.close()
    document = Document(parser.title.strip() or "Nuevo documento")
    document.clear()
    if not parser.paragraphs:
        return document
    for index, (alignment, runs) in enumerate(parser.paragraphs):
        if index == 0:
            document.paragraphs[0].alignment = alignment
            paragraph = document.paragraphs[0]
        else:
            document.add_paragraph(alignment=alignment)
            paragraph = document.paragraphs[-1]
        for text, style in runs:
            paragraph.append_text(text, style)
    return document


def _alignment_from_style(style: str) -> str:
    match = re.search(r"(?:^|;)text-align:(left|center|right|justify)(?:;|$)", style)
    return match.group(1) if match else "left"


def _style_from_inline_css(style: str) -> TextStyle:
    values = {}
    for declaration in style.split(";"):
        if ":" in declaration:
            key, value = declaration.split(":", 1)
            values[key.strip()] = value.strip()
    font_size = None
    size_match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)pt", values.get("font-size", ""))
    if size_match:
        font_size = float(size_match.group(1))
    return TextStyle(
        bold=values.get("font-weight") == "bold",
        italic=values.get("font-style") == "italic",
        underline=values.get("text-decoration") == "underline",
        font_family=values.get("font-family"),
        font_size=font_size,
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
