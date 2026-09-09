import pytest

from editor.model import Document, DocumentMetadata, Selection, TextStyle


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


def test_insert_text_between_styled_runs_keeps_run_order_and_styles() -> None:
    document = Document()
    document.insert_text("Hola", style=TextStyle(bold=True))
    document.insert_text(" mundo", style=TextStyle(italic=True))

    document.insert_text("!", position=4, style=TextStyle(underline=True))

    runs = document.paragraphs[0].runs
    assert [(run.text, run.style) for run in runs] == [
        ("Hola", TextStyle(bold=True)),
        ("!", TextStyle(underline=True)),
        (" mundo", TextStyle(italic=True)),
    ]


def test_apply_style_to_subrange_preserves_prefix_and_suffix() -> None:
    document = Document()
    document.insert_text("abcdef")

    document.apply_style(0, 2, 4, TextStyle(italic=True))

    assert [(run.text, run.style.italic) for run in document.paragraphs[0].runs] == [
        ("ab", False),
        ("cd", True),
        ("ef", False),
    ]


@pytest.mark.parametrize("alignment", ["left", "center", "right", "justify"])
def test_all_supported_alignments_are_accepted(alignment: str) -> None:
    document = Document()

    document.set_alignment(0, alignment)

    assert document.paragraphs[0].alignment == alignment


def test_metadata_is_retained_in_model_serialization() -> None:
    document = Document(
        metadata=DocumentMetadata(language="en", author="Test Author")
    )

    serialized = document.to_dict()

    assert serialized["metadata"] == {"language": "en", "author": "Test Author"}


@pytest.mark.parametrize(
    ("operation", "expected_exception"),
    [
        (lambda document: document.insert_text("x", paragraph_index=1), IndexError),
        (lambda document: document.insert_text("x", position=-1), ValueError),
        (lambda document: document.select_range(0, -1, 1), ValueError),
        (lambda document: document.set_font(Selection(0, 0, 0), "   "), ValueError),
    ],
)
def test_invalid_edit_operations_are_rejected(operation, expected_exception) -> None:
    with pytest.raises(expected_exception):
        operation(Document())


def test_style_update_merges_adjacent_runs_with_same_resulting_style() -> None:
    document = Document()
    document.insert_text("ab", style=TextStyle(bold=True))
    document.insert_text("cd", style=TextStyle(bold=False))

    document.apply_selection_style(
        document.select_range(0, 2, 4), TextStyle(bold=True)
    )

    assert len(document.paragraphs[0].runs) == 1
    assert document.paragraphs[0].runs[0].text == "abcd"
