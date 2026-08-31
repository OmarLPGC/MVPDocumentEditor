import pytest
from editor.model import Document


def test_document_creation():
    d = Document("Título de prueba")
    assert d.title == "Título de prueba"
    assert d.content == ""


def test_insert_and_clear():
    d = Document()
    d.insert_text("Hola")
    assert d.content == "Hola"
    d.insert_text(" Mundo")
    assert d.content == "Hola Mundo"
    d.clear()
    assert d.content == ""
