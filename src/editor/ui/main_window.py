"""Main editor window and the UI-to-model adapter."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QPlainTextEdit,
    QToolBar,
    QWidget,
)

from editor.io import DocumentIOError, load_document, save_document
from editor.model import Document


class EditorCanvas(QPlainTextEdit):
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
        """Render the model's plain text without creating a feedback loop."""

        self._syncing_from_model = True
        try:
            self.setPlainText(self.document_model.content)
        finally:
            self._syncing_from_model = False

    def _sync_model(self) -> None:
        if self._syncing_from_model:
            return
        self.document_model.clear()
        for index, paragraph in enumerate(self.toPlainText().split("\n")):
            if index == 0:
                self.document_model.insert_text(paragraph)
            else:
                self.document_model.add_paragraph(paragraph)

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
