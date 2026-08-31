from editor.model import Document


def run():
    d = Document("Título de prueba")
    assert d.title == "Título de prueba"
    assert d.content == ""

    d = Document()
    d.insert_text("Hola")
    assert d.content == "Hola"
    d.insert_text(" Mundo")
    assert d.content == "Hola Mundo"
    d.clear()
    assert d.content == ""


if __name__ == '__main__':
    run()
    print('SMOKE_TEST_PASSED')
