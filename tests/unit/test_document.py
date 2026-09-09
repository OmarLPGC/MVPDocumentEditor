import pytest

from editor.model import Document, Selection, TextStyle


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


def test_insert_text_at_position_preserves_existing_runs() -> None:
    document = Document()
    document.insert_text("H mundo")

    document.insert_text("ola", position=1)

    assert document.content == "Hola mundo"


def test_selection_can_apply_style_and_font_attributes() -> None:
    document = Document()
    document.insert_text("Texto")
    selection = document.select_range(0, 0, 5)

    document.apply_selection_style(selection, TextStyle(bold=True))
    document.set_font(selection, "Arial")
    document.set_font_size(selection, 14)

    style = document.paragraphs[0].runs[0].style
    assert style.bold is True
    assert style.font_family == "Arial"
    assert style.font_size == 14


def test_alignment_only_changes_selected_paragraph() -> None:
    document = Document()
    document.insert_text("Uno")
    document.add_paragraph("Dos")

    document.set_alignment(1, "center")

    assert document.paragraphs[0].alignment == "left"
    assert document.paragraphs[1].alignment == "center"


def test_invalid_selection_and_format_values_are_rejected() -> None:
    document = Document()
    document.insert_text("Texto")

    with pytest.raises(ValueError):
        document.select_range(0, 0, 99)
    with pytest.raises(ValueError):
        document.set_alignment(0, "diagonal")
    with pytest.raises(ValueError):
        document.set_font_size(Selection(0, 0, 5), 0)
