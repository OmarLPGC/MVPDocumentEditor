"""Strict validation for files before they enter the document pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import re
import struct
from typing import Final


class FileValidationError(ValueError):
    """Raised when an imported file violates the input security policy."""


@dataclass(frozen=True)
class FileValidationPolicy:
    """Limits and allowlists applied before processing an imported file."""

    max_html_bytes: int = 5 * 1024 * 1024
    max_image_bytes: int = 10 * 1024 * 1024
    max_image_pixels: int = 40_000_000
    allowed_html_extensions: frozenset[str] = frozenset({".html", ".htm"})
    allowed_image_extensions: frozenset[str] = frozenset(
        {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".webp"}
    )


DEFAULT_POLICY: Final = FileValidationPolicy()

_ACTIVE_URI = re.compile(r"^\s*(?:javascript|data|vbscript):", re.IGNORECASE)
_REMOTE_URI = re.compile(r"^\s*(?:https?|ftp):", re.IGNORECASE)
_HTML_FORBIDDEN_TAGS = frozenset(
    {"embed", "iframe", "link", "meta", "object", "script", "style"}
)
_HTML_FORBIDDEN_ATTRIBUTES = frozenset(
    {"action", "formaction", "href", "src", "srcdoc", "style"}
)


class _SafetyParser(HTMLParser):
    """Reject active content and externally loaded resources."""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized_tag = tag.casefold()
        if normalized_tag in _HTML_FORBIDDEN_TAGS:
            raise FileValidationError(
                f"HTML contains a forbidden element: <{normalized_tag}>"
            )

        for name, value in attrs:
            normalized_name = name.casefold()
            if normalized_name.startswith("on"):
                raise FileValidationError(
                    f"HTML contains an event handler attribute: {name}"
                )
            if normalized_name in _HTML_FORBIDDEN_ATTRIBUTES and value is not None:
                if _ACTIVE_URI.match(value) or _REMOTE_URI.match(value):
                    raise FileValidationError(
                        f"HTML contains a forbidden resource URI in {name}"
                    )
                if normalized_name == "style" and _REMOTE_URI.search(value):
                    raise FileValidationError(
                        "HTML contains a remote resource in an inline style"
                    )

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)


def _read_file(path: Path, max_bytes: int) -> bytes:
    if not path.is_file():
        raise FileValidationError(f"File does not exist: {path}")
    size = path.stat().st_size
    if size > max_bytes:
        raise FileValidationError(
            f"File exceeds the configured size limit of {max_bytes} bytes"
        )
    return path.read_bytes()


def _validate_html(path: Path, policy: FileValidationPolicy) -> None:
    content = _read_file(path, policy.max_html_bytes)
    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise FileValidationError("HTML must be valid UTF-8") from exc

    parser = _SafetyParser(convert_charrefs=True)
    try:
        parser.feed(decoded)
        parser.close()
    except (SyntaxError, ValueError) as exc:
        if isinstance(exc, FileValidationError):
            raise
        raise FileValidationError("HTML structure is invalid") from exc


def _image_dimensions(data: bytes, suffix: str) -> tuple[int, int]:
    if suffix == ".png" and data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if suffix in {".jpg", ".jpeg"} and data.startswith(b"\xff\xd8"):
        index = 2
        while index + 9 < len(data):
            if data[index] != 0xFF:
                index += 1
                continue
            marker = data[index + 1]
            index += 2
            if marker in {0xD8, 0xD9}:
                continue
            if index + 2 > len(data):
                break
            segment_length = struct.unpack(">H", data[index : index + 2])[0]
            if marker in range(0xC0, 0xC4) and index + 7 <= len(data):
                return struct.unpack(">HH", data[index + 3 : index + 7])
            index += segment_length
    if suffix == ".gif" and data[:6] in {b"GIF87a", b"GIF89a"} and len(data) >= 10:
        return struct.unpack("<HH", data[6:10])
    if suffix == ".bmp" and data.startswith(b"BM") and len(data) >= 26:
        return struct.unpack("<ii", data[18:26])
    if suffix == ".webp" and data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        if len(data) >= 30 and data[12:16] == b"VP8X":
            width = 1 + int.from_bytes(data[24:27], "little")
            height = 1 + int.from_bytes(data[27:30], "little")
            return width, height
    raise FileValidationError("Image content does not match a supported raster format")


def _validate_image(path: Path, policy: FileValidationPolicy) -> None:
    data = _read_file(path, policy.max_image_bytes)
    width, height = _image_dimensions(data, path.suffix.casefold())
    if width <= 0 or height <= 0:
        raise FileValidationError("Image dimensions must be positive")
    if width * height > policy.max_image_pixels:
        raise FileValidationError(
            f"Image exceeds the configured limit of {policy.max_image_pixels} pixels"
        )


def validate_file(
    path: str | Path, policy: FileValidationPolicy = DEFAULT_POLICY
) -> None:
    """Validate an import candidate, raising ``FileValidationError`` if unsafe."""

    candidate = Path(path)
    suffix = candidate.suffix.casefold()
    if suffix in policy.allowed_html_extensions:
        _validate_html(candidate, policy)
        return
    if suffix == ".svg":
        raise FileValidationError("SVG files are rejected by default")
    if suffix in policy.allowed_image_extensions:
        _validate_image(candidate, policy)
        return
    raise FileValidationError(f"Unsupported file type: {suffix or '<none>'}")
