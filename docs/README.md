# Editor de texto tipo Word (MVP)

Editor de documentos en Python desarrollado con **Spec-Driven Development (SDD)**.
El proyecto prioriza un modelo de documento independiente de la interfaz, entradas
validadas y una base de pruebas que permita evolucionar el editor de forma segura.

> **Estado actual:** el repositorio contiene el modelo de documento y la validación
> de archivos. La interfaz gráfica, la serialización HTML completa, la persistencia
> atómica y la recuperación de sesión están definidas como trabajo futuro; todavía
> no existe un ejecutable de escritorio listo para usuarios finales.

## Funcionalidad disponible

### Modelo de documento

El módulo `editor.model` no depende de Qt y puede utilizarse desde la aplicación o
desde pruebas:

- documentos con título y metadatos (`language`, `author`);
- párrafos con alineación `left`, `center`, `right` o `justify`;
- texto dividido en bloques (`TextRun`) con estilo propio;
- inserción de texto y creación de párrafos;
- selección de rangos y aplicación de negrita, cursiva, subrayado, fuente y tamaño;
- serialización de la estructura a un diccionario mediante `Document.to_dict()`;
- soporte para texto Unicode y preservación de los límites entre párrafos.

Ejemplo:

```python
from editor.model import Document, TextStyle

document = Document("Mi documento")
document.insert_text("Hola ")
document.insert_text("mundo", style=TextStyle(bold=True))
document.add_paragraph("Segundo párrafo", alignment="center")

selection = document.select_range(0, 0, 5)
document.set_font(selection, "Arial")
document.set_font_size(selection, 14)

print(document.content)
print(document.to_dict())
```

### Validación de archivos

`editor.validation.validate_file()` valida candidatos antes de que entren en la
pipeline de documentos:

- HTML y HTM en UTF-8, con un límite predeterminado de 5 MiB;
- imágenes raster BMP, GIF, JPEG, PNG y WebP, con un límite de 10 MiB y
  40 millones de píxeles;
- rechazo de SVG por defecto;
- rechazo de `script`, `iframe`, `object`, `embed`, recursos remotos, URI
  `javascript:`, `data:` y `vbscript:`, y atributos de eventos;
- verificación de que el contenido binario coincide con la extensión de la imagen.

Las reglas se pueden ajustar con `FileValidationPolicy`. Los errores se notifican
mediante `FileValidationError`; no se convierten silenciosamente en documentos
vacíos.

```python
from editor.validation import validate_file

validate_file("document.html")
```

## Requisitos

- Python 3.10 o posterior (hasta `<4.0`);
- `pip`;
- Windows, macOS o Linux para ejecutar el modelo y las pruebas.

PySide6 y Pillow son dependencias de la aplicación prevista. La GUI todavía no
está implementada, pero se instalan para mantener el entorno alineado con el
alcance del producto.

## Instalación para desarrollo

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r dev-requirements.txt
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r dev-requirements.txt
```

También existe configuración de Poetry en `pyproject.toml`, aunque el flujo
documentado y utilizado por CI usa `pip` y los ficheros de requisitos.

## Ejecutar pruebas y comprobaciones

La suite completa:

```bash
pytest
```

Incluye pruebas unitarias del modelo, persistencia básica y seguridad de entrada.
Para ejecutar únicamente una categoría:

```bash
pytest tests/unit
pytest tests/security
```

El smoke test del modelo puede ejecutarse directamente desde la raíz:

```bash
python tests/unit/run_document_smoketest.py
```

Comprobaciones de formato y estilo:

```bash
black src tests
isort src tests
flake8 src tests
```

La integración continua ejecuta `pytest -q` con Python 3.10 y 3.11 en pushes y
pull requests dirigidos a `main` o `master`.

## Estructura del repositorio

```text
.
├── src/editor/
│   ├── model/          # Modelo independiente de la UI
│   ├── validation/     # Política de validación de archivos
│   ├── io/             # Punto de extensión para entrada/salida
│   ├── serialization/  # Punto de extensión para serializadores
│   └── ui/             # Punto de extensión para la GUI
├── tests/
│   ├── unit/            # Comportamiento del modelo
│   ├── integration/     # Flujos entre capas
│   └── security/        # Casos de entrada insegura
├── specs/               # Requisitos funcionales y no funcionales
├── tasks/               # Historias y tareas de implementación
└── docs/                # Documentación de desarrollo y seguridad
```

## Alcance y próximos pasos

El MVP se está construyendo por capas. El plan contempla, en este orden:

1. completar el modelo, serialización y apertura/guardado HTML seguro;
2. añadir la GUI mínima con edición, selección y barra de herramientas;
3. implementar guardado atómico, copias de recuperación y limpieza de temporales;
4. incorporar imágenes y tablas básicas;
5. evaluar exportación PDF e interoperabilidad limitada con DOCX/ODT.

No forman parte del MVP la colaboración multiusuario, la sincronización en la
nube, la ejecución de contenido activo ni la edición avanzada de DOCX/ODT.

## Documentación relacionada

- [Configuración del entorno](dev-setup.md)
- [Política de seguridad](security-policy.md)
- [Especificaciones de aceptación](../specs/specs.md)
- [Plan de desarrollo](../specs/plan.md)
- [Constitución del proyecto](../specs/constitution.md)

Las contribuciones deben mantener la separación entre modelo, validación,
serialización, IO y UI, y añadir pruebas para cualquier comportamiento nuevo.
