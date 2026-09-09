import pytest
from PySide6.QtGui import QAction

from editor.model import Document, TextStyle
from editor.ui import MainWindow


def test_main_window_has_editable_new_document(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.windowTitle() == "Nuevo documento"
    assert window.editor.toPlainText() == ""
    assert window.editor.isEnabled()


def test_editor_updates_document_model_from_user_text(qtbot) -> None:
    window = MainWindow(Document("Prueba"))
    qtbot.addWidget(window)
    window.show()

    qtbot.keyClicks(window.editor, "Hola")
    qtbot.waitUntil(lambda: window.document_model.content == "Hola")

    assert window.document_model.content == "Hola"


def test_new_document_action_resets_editor(qtbot) -> None:
    window = MainWindow(Document("Prueba"))
    qtbot.addWidget(window)
    window.editor.setPlainText("Contenido anterior")

    window.new_document()

    assert window.windowTitle() == "Nuevo documento"
    assert window.editor.toPlainText() == ""
    assert window.document_model.content == ""


def test_unicode_keyboard_input_and_newlines_are_preserved(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    window.editor.setFocus()

    window.editor.insertPlainText("Español ñ € ✓")
    window.editor.insertPlainText("\nSegunda línea")

    assert window.editor.toPlainText() == "Español ñ € ✓\nSegunda línea"
    assert window.document_model.content == "Español ñ € ✓\nSegunda línea"
    assert len(window.document_model.paragraphs) == 2


def test_selection_can_be_replaced_and_deleted(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.editor.setPlainText("Texto temporal")
    cursor = window.editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(5, cursor.MoveMode.KeepAnchor)
    window.editor.setTextCursor(cursor)

    window.editor.insertPlainText("Nuevo")

    assert window.editor.toPlainText() == "Nuevo temporal"
    assert window.document_model.content == "Nuevo temporal"

    cursor = window.editor.textCursor()
    cursor.setPosition(5)
    cursor.setPosition(len(window.editor.toPlainText()), cursor.MoveMode.KeepAnchor)
    window.editor.setTextCursor(cursor)
    window.editor.delete_selection()

    assert window.editor.toPlainText() == "Nuevo"
    assert window.document_model.content == "Nuevo"


def test_cursor_status_reports_position_and_selection(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.editor.setPlainText("Hola\nMundo")
    cursor = window.editor.textCursor()
    cursor.setPosition(5)
    cursor.setPosition(10, cursor.MoveMode.KeepAnchor)
    window.editor.setTextCursor(cursor)

    assert window.editor.cursor_state() == (1, 5, 5)
    assert "Línea 2, columna 6" in window.statusBar().currentMessage()
    assert "5 seleccionados" in window.statusBar().currentMessage()


def test_window_save_and_open_round_trip(qtbot, tmp_path) -> None:
    window = MainWindow(Document("Original"))
    qtbot.addWidget(window)
    window.editor.setPlainText("Contenido guardado")
    path = tmp_path / "document.html"

    window.save_document(str(path))
    window.open_document(str(path))

    assert window.current_path == str(path)
    assert window.windowTitle() == "Original"
    assert window.editor.toPlainText() == "Contenido guardado"


def test_open_invalid_document_keeps_current_content(qtbot, tmp_path) -> None:
    window = MainWindow(Document("Actual"))
    qtbot.addWidget(window)
    window.editor.setPlainText("Contenido actual")
    path = tmp_path / "unsafe.html"
    path.write_text("<script>alert(1)</script>", encoding="utf-8")

    with pytest.raises(ValueError):
        window.open_document(str(path))

    assert window.editor.toPlainText() == "Contenido actual"
    assert window.document_model.content == "Contenido actual"


def test_toolbar_exposes_core_document_actions(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)

    action_names = {action.objectName() for action in window.findChildren(QAction)}

    assert {
        "newDocumentAction",
        "clearDocumentAction",
        "openDocumentAction",
        "saveDocumentAction",
    }.issubset(action_names)


def test_user_edit_save_clear_and_reopen_workflow(qtbot, tmp_path) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    window.editor.setFocus()
    path = tmp_path / "workflow.html"

    qtbot.keyClicks(window.editor, "Primera")
    window.editor.insertPlainText(" línea")
    window.editor.insertPlainText("\nSegunda línea ñ €")
    qtbot.waitUntil(
        lambda: window.document_model.content == "Primera línea\nSegunda línea ñ €"
    )
    window.save_document(str(path))
    window.clear_document()
    assert window.editor.toPlainText() == ""

    window.open_document(str(path))

    assert window.editor.toPlainText() == "Primera línea\nSegunda línea ñ €"
    assert window.document_model.content == "Primera línea\nSegunda línea ñ €"


def test_user_workflow_preserves_formatted_document_after_reopen(
    qtbot, tmp_path
) -> None:
    document = Document("Formato")
    document.insert_text(
        "Texto destacado",
        style=TextStyle(bold=True, italic=True, font_family="Arial", font_size=14),
    )
    window = MainWindow(document)
    qtbot.addWidget(window)
    path = tmp_path / "formatted.html"

    window.save_document(str(path))
    window.new_document()
    window.open_document(str(path))

    run = window.document_model.paragraphs[0].runs[0]
    assert window.editor.toPlainText() == "Texto destacado"
    assert run.style.bold is True
    assert run.style.italic is True
    assert run.style.font_family == "Arial"
    assert run.style.font_size == 14


def test_user_open_invalid_html_reports_error_without_replacing_document(
    qtbot, tmp_path
) -> None:
    window = MainWindow(Document("Actual"))
    qtbot.addWidget(window)
    window.editor.setPlainText("Contenido vigente")
    invalid_path = tmp_path / "malicious.html"
    invalid_path.write_text(
        '<p onclick="alert(1)">No debe abrirse</p>', encoding="utf-8"
    )

    with pytest.raises(ValueError):
        window.open_document(str(invalid_path))

    assert window.editor.toPlainText() == "Contenido vigente"
    assert window.windowTitle() == "Actual"


def test_format_actions_apply_visible_bold_to_selection(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.editor.setPlainText("Texto normal")
    cursor = window.editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(5, cursor.MoveMode.KeepAnchor)
    window.editor.setTextCursor(cursor)

    window.bold_action.trigger()

    assert window.editor.textCursor().hasSelection()
    assert window.editor.textCursor().charFormat().fontWeight() == 700
    assert window.document_model.paragraphs[0].runs[0].style.bold is True


def test_format_toggle_is_inherited_by_following_text(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.editor.setFocus()

    window.bold_action.trigger()
    window.editor.insertPlainText("Texto nuevo")

    assert window.editor.toPlainText() == "Texto nuevo"
    assert window.document_model.paragraphs[0].runs[0].style.bold is True


def test_all_basic_format_actions_are_exposed(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)

    action_names = {action.objectName() for action in window.findChildren(QAction)}

    assert {
        "boldFormatAction",
        "italicFormatAction",
        "underlineFormatAction",
    }.issubset(action_names)


def test_font_family_and_size_apply_to_selected_text(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.editor.setPlainText("Texto")
    cursor = window.editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(5, cursor.MoveMode.KeepAnchor)
    window.editor.setTextCursor(cursor)

    window.set_font_family("Arial")
    window.set_font_size(18)

    style = window.document_model.paragraphs[0].runs[0].style
    assert style.font_family
    assert style.font_size == 18


def test_unavailable_font_uses_safe_fallback(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.editor.setPlainText("Texto")
    cursor = window.editor.textCursor()
    cursor.setPosition(0)
    cursor.setPosition(5, cursor.MoveMode.KeepAnchor)
    window.editor.setTextCursor(cursor)

    window.set_font_family("FontThatDoesNotExist_987654")

    style = window.document_model.paragraphs[0].runs[0].style
    assert style.font_family == window.font_combo.currentText()
    assert style.font_family != "FontThatDoesNotExist_987654"


def test_font_controls_apply_to_text_typed_after_cursor_formatting(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    window.editor.setFocus()

    window.set_font_family("Arial")
    window.set_font_size(16)
    window.editor.insertPlainText("Texto nuevo")

    style = window.document_model.paragraphs[0].runs[0].style
    assert style.font_family == window.font_combo.currentText()
    assert style.font_size == 16
