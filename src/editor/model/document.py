class Document:
    """Minimal document model placeholder for the project structure.

    The actual implementation will evolve to include paragraphs, styles,
    validation rules, and serialization logic.
    """

    def __init__(self, title: str = "Nuevo documento"):
        self.title = title
        self.content = ""

    def insert_text(self, text: str) -> None:
        self.content += text

    def clear(self) -> None:
        self.content = ""
