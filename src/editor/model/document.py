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


@dataclass(frozen=True)
class Selection:
    """A half-open text range within one paragraph."""

    paragraph_index: int
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.paragraph_index < 0:
            raise ValueError("Paragraph index cannot be negative")
        if self.start < 0 or self.end < self.start:
            raise ValueError("Selection range is invalid")


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
        self.insert_text(len(self.text), text, style)

    def insert_text(
        self, position: int, text: str, style: TextStyle | None = None
    ) -> None:
        if not text:
            return
        if position < 0 or position > len(self.text):
            raise ValueError("Text position is outside the paragraph")
        style = style or TextStyle()
        if position == len(self.text):
            if self.runs and self.runs[-1].style == style:
                self.runs[-1] = TextRun(self.runs[-1].text + text, style)
            else:
                self.runs.append(TextRun(text, style))
            return

        updated: list[TextRun] = []
        offset = 0
        inserted = False
        for run in self.runs:
            run_end = offset + len(run.text)
            if not inserted and position <= run_end:
                local_position = position - offset
                if local_position == 0:
                    updated.append(TextRun(text, style))
                    updated.append(run)
                elif local_position == len(run.text):
                    updated.append(run)
                    updated.append(TextRun(text, style))
                else:
                    updated.extend(
                        (
                            TextRun(run.text[:local_position], run.style),
                            TextRun(text, style),
                            TextRun(run.text[local_position:], run.style),
                        )
                    )
                inserted = True
            else:
                updated.append(run)
            offset = run_end
        self.runs = updated

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
        position: int | None = None,
        style: TextStyle | None = None,
    ) -> None:
        """Insert text at a position, defaulting to the end of a paragraph."""

        paragraph = self._paragraph_at(
            len(self.paragraphs) - 1
            if paragraph_index is None
            else paragraph_index
        )
        paragraph.insert_text(
            len(paragraph.text) if position is None else position, text, style
        )

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

    def select_range(self, paragraph_index: int, start: int, end: int) -> Selection:
        """Create and validate a selection for subsequent editing operations."""

        paragraph = self._paragraph_at(paragraph_index)
        selection = Selection(paragraph_index, start, end)
        if selection.end > len(paragraph.text):
            raise ValueError("Selection range is outside the paragraph")
        return selection

    def apply_selection_style(self, selection: Selection, style: TextStyle) -> None:
        """Apply a complete style to a previously selected range."""

        self._validate_selection(selection)
        self.apply_style(
            selection.paragraph_index, selection.start, selection.end, style
        )

    def set_font(self, selection: Selection, font_family: str) -> None:
        """Change the font while preserving other style attributes."""

        if not font_family.strip():
            raise ValueError("Font family cannot be empty")
        self._update_selection_style(
            selection, lambda style: replace(style, font_family=font_family)
        )

    def set_font_size(self, selection: Selection, font_size: float) -> None:
        """Change the font size while preserving other style attributes."""

        if font_size <= 0:
            raise ValueError("Font size must be positive")
        self._update_selection_style(
            selection, lambda style: replace(style, font_size=font_size)
        )

    def set_alignment(self, paragraph_index: int, alignment: str) -> None:
        """Set alignment for exactly one paragraph."""

        paragraph = self._paragraph_at(paragraph_index)
        if alignment not in Paragraph.ALLOWED_ALIGNMENTS:
            raise ValueError(f"Unsupported paragraph alignment: {alignment}")
        paragraph.alignment = alignment

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

    def _validate_selection(self, selection: Selection) -> None:
        paragraph = self._paragraph_at(selection.paragraph_index)
        if selection.end > len(paragraph.text):
            raise ValueError("Selection range is outside the paragraph")

    def _update_selection_style(
        self, selection: Selection, update: Any
    ) -> None:
        self._validate_selection(selection)
        paragraph = self._paragraph_at(selection.paragraph_index)
        updated_runs: list[TextRun] = []
        position = 0
        for run in paragraph.runs:
            run_start = position
            run_end = position + len(run.text)
            position = run_end
            if run_end <= selection.start or run_start >= selection.end:
                updated_runs.append(run)
                continue
            before = run.text[: max(0, selection.start - run_start)]
            selected_start = max(0, selection.start - run_start)
            selected_end = min(len(run.text), selection.end - run_start)
            selected = run.text[selected_start:selected_end]
            after = run.text[selected_end:]
            if before:
                updated_runs.append(TextRun(before, run.style))
            if selected:
                updated_runs.append(TextRun(selected, update(run.style)))
            if after:
                updated_runs.append(TextRun(after, run.style))
        paragraph.runs = self._merge_adjacent_runs(updated_runs)

    @staticmethod
    def _merge_adjacent_runs(runs: list[TextRun]) -> list[TextRun]:
        merged: list[TextRun] = []
        for run in runs:
            if merged and merged[-1].style == run.style:
                merged[-1] = replace(merged[-1], text=merged[-1].text + run.text)
            else:
                merged.append(run)
        return merged
