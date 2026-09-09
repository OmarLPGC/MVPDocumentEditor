"""Main editor window and the UI-to-model adapter."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, QFont, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QTextEdit,
    QToolBar,
    QWidget,
)

from editor.io import DocumentIOError, load_document, save_document
from editor.model import Document, TextStyle
from editor.serialization import serialize_document


class EditorCanvas(QTextEdit):
    """Text canvas that keeps a framework-independent Document in sync."""

    cursor_state_changed = Signal(tuple)

    def __init__(self, document: Document, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.document_model = document
        self.setObjectName("editorCanvas")
        self.setPlaceholderText("Empieza a escribir tu documento…")
        self.setTabChangesFocus(False)
        self.document().contentsChanged.connect(self._sync_model)
        self._syncing_from_model = False
        self.cursorPositionChanged.connect(self._notify_cursor_state)
        self.selectionChanged.connect(self._notify_cursor_state)

    def load_model(self) -> None:
        """Render model text and styles without creating a feedback loop."""

        self._syncing_from_model = True
        try:
            self.setHtml(serialize_document(self.document_model))
            if self.toPlainText().endswith(" ") and not self.document_model.content.endswith(
                " "
            ):
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.End)
                cursor.deletePreviousChar()
                self.setTextCursor(cursor)
        finally:
            self._syncing_from_model = False

    def _sync_model(self) -> None:
        if self._syncing_from_model:
            return
        self.document_model.clear()
        block = self.document().firstBlock()
        index = 0
        while block.isValid():
            if index == 0:
                paragraph = self.document_model.paragraphs[0]
            else:
                self.document_model.add_paragraph()
                paragraph = self.document_model.paragraphs[-1]
            paragraph.alignment = self._alignment_name(block.blockFormat().alignment())
            iterator = block.begin()
            while not iterator.atEnd():
                fragment = iterator.fragment()
                if fragment.isValid() and fragment.text():
                    paragraph.append_text(
                        fragment.text(), self._style_from_format(fragment.charFormat())
                    )
                iterator += 1
            block = block.next()
            index += 1

    @staticmethod
    def _alignment_name(alignment: int) -> str:
        return {
            1: "left",
            2: "center",
            4: "right",
            8: "justify",
        }.get(int(alignment), "left")

    @staticmethod
    def _style_from_format(char_format: QTextCharFormat) -> TextStyle:
        font = char_format.font()
        return TextStyle(
            bold=font.bold(),
            italic=font.italic(),
            underline=font.underline(),
            font_family=font.family() or None,
            font_size=font.pointSizeF() if font.pointSizeF() > 0 else None,
        )

    def apply_format(self, char_format: QTextCharFormat) -> None:
        cursor = self.textCursor()
        cursor.mergeCharFormat(char_format)
        self.setTextCursor(cursor)
        self.setFocus()

    def cursor_state(self) -> tuple[int, int, int]:
        """Return zero-based line, column, and selected character count."""

        cursor = self.textCursor()
        return (
            cursor.blockNumber(),
            cursor.positionInBlock(),
            len(cursor.selectedText()),
        )

    def delete_selection(self) -> None:
        """Delete the current selection and keep the editor focused."""

        cursor = self.textCursor()
        if not cursor.hasSelection():
            return
        cursor.removeSelectedText()
        self.setTextCursor(cursor)
        self.setFocus()

    def _notify_cursor_state(self) -> None:
        self.cursor_state_changed.emit(self.cursor_state())


class MainWindow(QMainWindow):
    """Minimal, testable editor shell for a new document."""

    def __init__(
        self, document: Document | None = None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.document_model = document or Document()
        self.current_path: str | None = None
        self.setObjectName("mainWindow")
        self.setWindowTitle(self.document_model.title)
        self.resize(960, 700)
        self._build_ui()

    def _build_ui(self) -> None:
        self._build_toolbar()
        self.editor = EditorCanvas(self.document_model, self)
        self.editor.cursor_state_changed.connect(self._update_cursor_status)
        self.editor.setFont(QFont("Segoe UI", 12))
        self.editor.load_model()
        self.setCentralWidget(self.editor)
        self._update_cursor_status(self.editor.cursor_state())

    def _update_cursor_status(self, state: tuple[int, int, int]) -> None:
        line, column, selected = state
        selection_text = f" · {selected} seleccionados" if selected else ""
        self.statusBar().showMessage(
            f"Línea {line + 1}, columna {column + 1}{selection_text}"
        )

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Edición", self)
        toolbar.setObjectName("editingToolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        new_action = QAction("Nuevo", self)
        new_action.setObjectName("newDocumentAction")
        new_action.triggered.connect(self.new_document)
        toolbar.addAction(new_action)

        clear_action = QAction("Limpiar", self)
        clear_action.setObjectName("clearDocumentAction")
        clear_action.triggered.connect(self.clear_document)
        toolbar.addAction(clear_action)

        open_action = QAction("Abrir", self)
        open_action.setObjectName("openDocumentAction")
        open_action.triggered.connect(self.open_from_dialog)
        toolbar.addAction(open_action)

        save_action = QAction("Guardar", self)
        save_action.setObjectName("saveDocumentAction")
        save_action.triggered.connect(self.save_from_dialog)
        toolbar.addAction(save_action)

        self.bold_action = self._format_action(
            toolbar, "Negrita", "boldFormatAction", self.toggle_bold
        )
        self.italic_action = self._format_action(
            toolbar, "Cursiva", "italicFormatAction", self.toggle_italic
        )
        self.underline_action = self._format_action(
            toolbar, "Subrayado", "underlineFormatAction", self.toggle_underline
        )

    @staticmethod
    def _format_action(
        toolbar: QToolBar, label: str, object_name: str, callback
    ) -> QAction:
        action = QAction(label, toolbar)
        action.setObjectName(object_name)
        action.setCheckable(True)
        action.triggered.connect(callback)
        toolbar.addAction(action)
        return action

    def _toggle_format(self, attribute: str, checked: bool) -> None:
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            current = cursor.charFormat()
            updated = QTextCharFormat()
            updated.setFont(current.font())
            if attribute == "bold":
                updated.setFontWeight(QFont.Weight.Bold if checked else QFont.Weight.Normal)
            elif attribute == "italic":
                updated.setFontItalic(checked)
            else:
                updated.setFontUnderline(checked)
            self.editor.apply_format(updated)
            return

        current = cursor.charFormat()
        updated = QTextCharFormat()
        updated.setFont(current.font())
        if attribute == "bold":
            updated.setFontWeight(QFont.Weight.Bold if checked else QFont.Weight.Normal)
        elif attribute == "italic":
            updated.setFontItalic(checked)
        else:
            updated.setFontUnderline(checked)
        self.editor.apply_format(updated)

    def toggle_bold(self, checked: bool) -> None:
        self._toggle_format("bold", checked)

    def toggle_italic(self, checked: bool) -> None:
        self._toggle_format("italic", checked)

    def toggle_underline(self, checked: bool) -> None:
        self._toggle_format("underline", checked)

    def new_document(self) -> None:
        self.document_model = Document()
        self.setWindowTitle(self.document_model.title)
        self.editor.document_model = self.document_model
        self.editor.load_model()
        self.editor.setFocus()

    def clear_document(self) -> None:
        self.editor.clear()
        self.editor.setFocus()

    def save_document(self, path: str) -> None:
        """Save the current model and update the active path."""

        save_document(self.document_model, path)
        self.current_path = path

    def open_document(self, path: str) -> None:
        """Open a validated document, preserving current state on failure."""

        loaded = load_document(path)
        self.document_model = loaded
        self.current_path = path
        self.setWindowTitle(loaded.title)
        self.editor.document_model = loaded
        self.editor.load_model()
        self.editor.setFocus()

    def save_from_dialog(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar documento", "", "HTML (*.html *.htm)"
        )
        if path:
            self.save_document(path)

    def open_from_dialog(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Abrir documento", "", "HTML (*.html *.htm)"
        )
        if path:
            try:
                self.open_document(path)
            except DocumentIOError as exc:
                self.statusBar().showMessage(str(exc), 5000)


def create_main_window(document: Document | None = None) -> MainWindow:
    """Create the main window through a small factory suitable for tests."""

    return MainWindow(document=document)
