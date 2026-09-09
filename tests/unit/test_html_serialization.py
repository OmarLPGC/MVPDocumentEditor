from editor.model import Document, TextStyle
from editor.serialization import serialize_document


def test_serializes_text_and_paragraph_alignment() -> None:
    document = Document("Documento de prueba")
    document.insert_text("Hola")
    document.add_paragraph("Adiós", alignment="center")

    html = serialize_document(document)

    assert "<p style=\"text-align:left\">Hola</p>" in html
    assert '<p style="text-align:center">Adiós</p>' in html
    assert "<script" not in html


def test_serializes_allowed_inline_text_styles() -> None:
    document = Document()
    document.insert_text(
        "Formato",
        style=TextStyle(
            bold=True,
            italic=True,
            underline=True,
            font_family="Arial",
            font_size=14,
        ),
    )

    html = serialize_document(document)

    assert "font-weight:bold" in html
    assert "font-style:italic" in html
    assert "text-decoration:underline" in html
    assert "font-family:Arial" in html
    assert "font-size:14pt" in html


def test_escapes_html_text_and_title() -> None:
    document = Document('<Título & "seguro">')
    document.insert_text("<script>alert('x')</script> & texto")

    html = serialize_document(document)

    assert "&lt;script&gt;alert('x')&lt;/script&gt; &amp; texto" in html
    assert "&lt;Título &amp; &quot;seguro&quot;&gt;" in html
    assert "<script" not in html


def test_unsafe_font_value_is_omitted() -> None:
    document = Document()
    document.insert_text(
        "Texto",
        style=TextStyle(font_family='Arial"; color:red; /*'),
    )

    html = serialize_document(document)

    assert "font-family" not in html
    assert "color:red" not in html
