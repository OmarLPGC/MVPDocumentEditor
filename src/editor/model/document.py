"""Framework-independent document model."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from typing import Any


@dataclass(frozen=True)
class TextStyle:
    """Formatting attributes supported by the document model."""

    bold: bool = False
    italic: bool = False
    underline: bool = False
    font_family: str | None = None
    font_size: float | None = None


@dataclass(frozen=True)
class TextRun:
    """A contiguous piece of text sharing one style."""

    text: str
    style: TextStyle = field(default_factory=TextStyle)

    def __post_init__(self) -> None:
        if not self.text:
            raise ValueError("A text run cannot be empty")


@dataclass
class Paragraph:
    """A paragraph containing ordered styled text runs."""

    runs: list[TextRun] = field(default_factory=list)
    alignment: str = "left"

    ALLOWED_ALIGNMENTS = frozenset({"left", "center", "right", "justify"})

    def __post_init__(self) -> None:
        if self.alignment not in self.ALLOWED_ALIGNMENTS:
            raise ValueError(f"Unsupported paragraph alignment: {self.alignment}")

    @property
    def text(self) -> str:
        return "".join(run.text for run in self.runs)

    def append_text(self, text: str, style: TextStyle | None = None) -> None:
        if not text:
            return
        style = style or TextStyle()
        if self.runs and self.runs[-1].style == style:
            self.runs[-1] = TextRun(self.runs[-1].text + text, style)
        else:
            self.runs.append(TextRun(text, style))

    def to_dict(self) -> dict[str, Any]:
        return {
            "alignment": self.alignment,
            "runs": [
                {"text": run.text, "style": asdict(run.style)} for run in self.runs
            ],
        }


@dataclass
class DocumentMetadata:
    """Metadata that does not affect document content or rendering."""

    language: str = "es"
    author: str | None = None


class Document:
    """Structured document model independent from Qt and the UI."""

    def __init__(
        self,
        title: str = "Nuevo documento",
        *,
        metadata: DocumentMetadata | None = None,
    ) -> None:
        if not title.strip():
            raise ValueError("Document title cannot be empty")
        self.title = title
        self.metadata = metadata or DocumentMetadata()
        self.paragraphs: list[Paragraph] = [Paragraph()]

    @property
    def content(self) -> str:
        """Return plain text, preserving paragraph boundaries with newlines."""

        return "\n".join(paragraph.text for paragraph in self.paragraphs)

    def insert_text(
        self,
        text: str,
        *,
        paragraph_index: int | None = None,
        style: TextStyle | None = None,
    ) -> None:
        """Append text to a paragraph; retained as the initial editing API."""

        paragraph = self._paragraph_at(
            len(self.paragraphs) - 1
            if paragraph_index is None
            else paragraph_index
        )
        paragraph.append_text(text, style)

    def add_paragraph(
        self, text: str = "", *, alignment: str = "left"
    ) -> int:
        paragraph = Paragraph(alignment=alignment)
        paragraph.append_text(text)
        self.paragraphs.append(paragraph)
        return len(self.paragraphs) - 1

    def apply_style(
        self,
        paragraph_index: int,
        start: int,
        end: int,
        style: TextStyle,
    ) -> None:
        """Apply ``style`` to a half-open character range in one paragraph."""

        paragraph = self._paragraph_at(paragraph_index)
        if start < 0 or end < start or end > len(paragraph.text):
            raise ValueError("Text range is outside the paragraph")
        if start == end:
            return

        styled_runs: list[TextRun] = []
        position = 0
        for run in paragraph.runs:
            run_start = position
            run_end = position + len(run.text)
            position = run_end
            if run_end <= start or run_start >= end:
                styled_runs.append(run)
                continue
            before = run.text[: max(0, start - run_start)]
            selected = run.text[max(0, start - run_start) : min(len(run.text), end - run_start)]
            after = run.text[min(len(run.text), end - run_start) :]
            if before:
                styled_runs.append(TextRun(before, run.style))
            if selected:
                styled_runs.append(TextRun(selected, style))
            if after:
                styled_runs.append(TextRun(after, run.style))
        paragraph.runs = self._merge_adjacent_runs(styled_runs)

    def clear(self) -> None:
        self.paragraphs = [Paragraph()]

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-ready representation without UI objects."""

        return {
            "title": self.title,
            "metadata": asdict(self.metadata),
            "paragraphs": [paragraph.to_dict() for paragraph in self.paragraphs],
        }

    def _paragraph_at(self, index: int) -> Paragraph:
        if not 0 <= index < len(self.paragraphs):
            raise IndexError(f"Paragraph index out of range: {index}")
        return self.paragraphs[index]

    @staticmethod
    def _merge_adjacent_runs(runs: list[TextRun]) -> list[TextRun]:
        merged: list[TextRun] = []
        for run in runs:
            if merged and merged[-1].style == run.style:
                merged[-1] = replace(merged[-1], text=merged[-1].text + run.text)
            else:
                merged.append(run)
        return merged
