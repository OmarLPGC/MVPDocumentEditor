from pathlib import Path

import pytest

from editor.validation import FileValidationError, FileValidationPolicy, validate_file


def test_valid_html_is_accepted(tmp_path: Path) -> None:
    path = tmp_path / "document.html"
    path.write_text("<p>Hola, edición segura</p>", encoding="utf-8")

    validate_file(path)


def test_html_must_be_valid_utf8(tmp_path: Path) -> None:
    path = tmp_path / "document.html"
    path.write_bytes(b"<p>\xff</p>")

    with pytest.raises(FileValidationError, match="UTF-8"):
        validate_file(path)


@pytest.mark.parametrize(
    "content",
    [
        "<script>alert('x')</script>",
        '<img src="https://example.com/image.png">',
        '<p onclick="alert(1)">texto</p>',
        '<a href="javascript:alert(1)">enlace</a>',
    ],
)
def test_unsafe_html_is_rejected(tmp_path: Path, content: str) -> None:
    path = tmp_path / "document.html"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(FileValidationError):
        validate_file(path)


def test_svg_is_rejected_by_default(tmp_path: Path) -> None:
    path = tmp_path / "image.svg"
    path.write_text("<svg><script>alert(1)</script></svg>", encoding="utf-8")

    with pytest.raises(FileValidationError, match="SVG"):
        validate_file(path)


def test_oversized_html_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "large.html"
    path.write_text("x" * 101, encoding="utf-8")
    policy = FileValidationPolicy(max_html_bytes=100)

    with pytest.raises(FileValidationError, match="size limit"):
        validate_file(path, policy)


def test_image_extension_must_match_raster_content(tmp_path: Path) -> None:
    path = tmp_path / "image.png"
    path.write_bytes(b"not a png")

    with pytest.raises(FileValidationError, match="supported raster"):
        validate_file(path)


def test_unsupported_extension_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "document.docm"
    path.write_bytes(b"content")

    with pytest.raises(FileValidationError, match="Unsupported"):
        validate_file(path)
