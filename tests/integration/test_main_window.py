import pytest

from editor.model import Document
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
