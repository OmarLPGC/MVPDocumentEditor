import pytest

from editor.model import Document, TextStyle


def test_document_creation() -> None:
    d = Document("Título de prueba")
    assert d.title == "Título de prueba"
    assert d.content == ""


def test_insert_and_clear() -> None:
    d = Document()
    d.insert_text("Hola")
    assert d.content == "Hola"
    d.insert_text(" Mundo")
    assert d.content == "Hola Mundo"
    d.clear()
    assert d.content == ""


def test_document_preserves_unicode_content() -> None:
    document = Document()

    document.insert_text("Español — edición básica ✓")

    assert document.content == "Español — edición básica ✓"


def test_empty_document_has_one_empty_paragraph() -> None:
    document = Document()

    assert document.content == ""
    assert len(document.paragraphs) == 1
    assert document.paragraphs[0].runs == []


def test_document_preserves_paragraph_boundaries() -> None:
    document = Document()
    document.insert_text("Primero")
    document.add_paragraph("Segundo")

    assert document.content == "Primero\nSegundo"


def test_apply_style_changes_only_the_selected_range() -> None:
    document = Document()
    document.insert_text("Hola mundo")

    document.apply_style(0, 0, 4, TextStyle(bold=True))

    assert document.paragraphs[0].runs[0].text == "Hola"
    assert document.paragraphs[0].runs[0].style.bold is True
    assert document.paragraphs[0].runs[1].text == " mundo"
    assert document.paragraphs[0].runs[1].style.bold is False


def test_document_serialization_shape_is_ui_independent() -> None:
    document = Document("Mi documento")
    document.insert_text("Texto", style=TextStyle(italic=True))

    serialized = document.to_dict()

    assert serialized["title"] == "Mi documento"
    assert serialized["paragraphs"][0]["runs"][0]["style"]["italic"] is True


@pytest.mark.parametrize("invalid_title", ["", "   "])
def test_document_rejects_empty_title(invalid_title: str) -> None:
    with pytest.raises(ValueError, match="title"):
        Document(invalid_title)
