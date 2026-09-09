"""Run the desktop editor with ``python -m editor``."""

import sys

from PySide6.QtWidgets import QApplication

from editor.ui import create_main_window


def main() -> int:
    app = QApplication(sys.argv)
    window = create_main_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
