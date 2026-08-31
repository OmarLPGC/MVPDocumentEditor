# Plan de desarrollo — Editor de texto tipo Word (SDD)

1. Resumen
----------
Este documento define el plan de desarrollo de alto nivel para un editor de texto de estilo Word usando Python y siguiendo Spec-Driven Development (SDD). El enfoque principal ya no es solo “funcionalidad”, sino capacidad de entrega con robustez, seguridad, trazabilidad y mantenimiento a largo plazo.

La base del proyecto es:
- un modelo de documento interno robusto y desacoplado de la capa de vista
- serialización segura y validada
- validación estricta de entradas de archivo
- pruebas automatizadas por capas
- recuperación y seguridad por defecto

2. Visión y objetivos
---------------------
Construir un editor de texto de escritorio capaz de:
- crear y editar texto con formato básico
- trabajar con fuentas, tamaños y alineaciones
- manejar imágenes y tablas básicas
- abrir y guardar documentos con un formato seguro y validado
- mantener integridad del contenido bajo errores, cierres inesperados o archivos corruptos
- exportar a PDF y soportar interoperabilidad limitada con DOCX/ODT

El objetivo del producto es ofrecer una base usable y segura para un editor de estilo Word, no un editor de documentos “todo vale” con riesgos no controlados.

3. Principios de ingeniería
---------------------------
- Seguridad por defecto: todo archivo importado se valida antes de procesarse.
- Modelo interno canónico: la lógica de negocio no dependerá del renderizador de Qt.
- HTML como formato de intercambio, no como modelo de verdad absoluto.
- Guardado atómico y recuperación de estado para evitar pérdida de trabajo.
- Separación radical entre lógica, serialización, validación, IO y UI.
- Desarrollo guiado por tests y especificaciones ejecutables.

4. Elección de tecnologías (propuesta)
--------------------------------------
- Lenguaje: Python 3.10+
- GUI: PySide6 (Qt for Python)
- Modelo de documento: representación interna estructurada y adaptador sobre QTextDocument/QTextCursor
- Serialización: HTML seguro con sanitización y normalización estricta; JSON como representación interna si hace falta
- Imágenes: Pillow con validación de tipo, tamaño y dimensiones
- Import/export DOCX/ODT: python-docx o librerías equivalentes solo para alcance limitado; no como pieza central del MVP
- Tests: pytest, pytest-qt, hypothesis (cuando aplique)
- Gestión de paquetes: poetry o venv + pip
- CI: GitHub Actions
- Linter / formatting: black, isort, flake8

5. Enfoque SDD reforzado
------------------------
1. Definir especificaciones funcionales y de seguridad en specs/specs.md.
2. Convertir cada historia funcional en tests de aceptación automatizables.
3. Añadir casos de seguridad y manejo de errores como requisitos de aceptación, no como tareas laterales.
4. Implementar el MVP mínimo y verificar con tests unitarios, de integración y de seguridad.
5. Repetir iterativamente, ampliando funcionalidad con la misma disciplina de calidad.

6. Fases y hitos
----------------
6.1 Fase 0 — Preparación y base de seguridad
- Crear repositorio con estructura limpia
- Definir entorno Python y dependencias
- CI mínima con pytest
- Convención de commits y revisión de PRs
- Definir política inicial de seguridad para archivos importados
- Definir límites de tamaño y tipo de archivos soportados

Entregables:
- proyecto con repo inicial
- CI funcionando
- primer conjunto de requisitos de seguridad escritos y aceptados

6.2 Fase 1 — Modelo de documento y capa de negocio
- Diseñar un modelo interno del documento
- Definir estructura de bloques, texto, estilo y metadatos
- Separar la lógica de negocio de la capa UI
- Implementar pruebas de serialización y formato básico

Entregables:
- document model con API estable y testeable
- pruebas unitarias para serialización y estilo

6.3 Fase 2 — Editor GUI mínimo
- Crear ventana principal, barra de herramientas y canvas de edición
- Implementar escritura básica y selección de texto
- Ajustar foco, teclado y edición general
- Añadir comportamiento base de guardado/abrir

Entregables:
- editor ejecutable de base
- flujo MVP de edición y guardado

6.4 Fase 3 — Formateo y alineación
- Negrita, cursiva, subrayado
- Cambio de fuente y tamaño
- Alineación horizontal de párrafos
- Aplicación a selección o al texto posterior

Entregables:
- edición con formato funcional
- pruebas de integración para los cambios

6.5 Fase 4 — Seguridad, validación y recuperación
- Validación de entrada de HTML e imágenes
- Sanitización de salida HTML
- Guardado atómico y recuperación de sesión
- Borrado seguro de temporales

Entregables:
- flujo de archivo seguro
- pruebas de seguridad y recuperación

6.6 Fase 5 — Imágenes, tablas y ajustes avanzados
- Inserción de imágenes permitidas
- Ajuste básico de ancho/posición
- Tablas sencillas
- Estilos de párrafo y títulos

Entregables:
- soporte básico para contenido más complejo
- validación con tests de integración

6.7 Fase 6 — Exportación y compatibilidad
- Exportar PDF
- Importar/exportar DOCX/ODT mínimo
- Validar compatibilidad con contenido simple

Entregables:
- export a PDF funcional
- import/export de DOCX/ODT con alcance limitado

6.8 Fase 7 — Calidad, QA y release
- Tests de aceptación completos
- QA manual documentado
- Guía de usuario y advertencias de soportes limitados
- Empaquetado y release

Entregables:
- versión estable de release candidate
- documentación mínima publicable

7. Tareas desglosadas por fase
------------------------------
- Preparar entorno y plantilla de proyecto
- Diseñar API interna para el document model
- Definir validación de tipo, tamaño y seguridad para archivos de entrada
- Implementar guardado atómico y backup temporal
- Implementar GUI mínima con documento vacío
- Implementar guardado/abrir en HTML seguro
- Añadir formateo básico y toolbar
- Añadir imágenes y tablas básicas
- Añadir validación de seguridad e import/export filtros
- Implementar undo/redo y clipboard
- Integrar export PDF y compatibilidad DOCX/ODT de alcance limitado
- Escribir tests unitarios, de integración y de seguridad
- Configurar CI de PRs con ejecución automatizada
- Documentar guía de usuario y limitaciones de formatos
- Empaquetado y release

8. Riesgos clave y mitigaciones
-----------------------------
8.1 Riesgos de seguridad
- HTML importado con contenido malicioso
  - Mitigación: parser seguro, sanitización estricta, bloqueo de scripts y URLs externas
- SVG e imágenes con contenido activo
  - Mitigación: rechazo por defecto, validación del tipo de contenido real
- ZIP/ODT/DOCX maliciosos o extremadamente grandes
  - Mitigación: límites de tamaño, validación de estructura, detección de ZIP bomb

8.2 Riesgos de robustez funcional
- Documentos corruptos o guardados parcialmente
  - Mitigación: guardado atómico, backup temporal y recuperación
- Falla de UI por lógica acoplada
  - Mitigación: capas separadas y tests intensivos de negocio
- Frágil CI o tests inestables
  - Mitigación: tests deterministas y separación lógica/GUI

8.3 Riesgos de producto
- HTML como único formato de intercambio no es suficiente para largo plazo
  - Mitigación: mantener un modelo interno independiente y documentar HTML como export/import compatible
- Documentos complejos pueden no renderizar igual en distintos entornos
  - Mitigación: restringir alcance del MVP y documentar compatibilidad

9. Criterios de salida por hito
------------------------------
Hito 1: MVP seguro y funcional
- documento editable y persistente
- formato básico funcional
- guardado/abrir HTML seguro
- recuperación básica y validación de entrada

Hito 2: edición rica con validación
- imágenes permitidas y tablas básicas
- formateo extendido
- pruebas de seguridad sobre archivos e importación

Hito 3: compatibilidad y release
- PDF funcional
- DOCX/ODT básico con limitaciones documentadas
- tests automatizados completos
- CI estable y guía de usuario aprobada

10. Siguientes pasos
-------------------
- Confirmar la política de formatos: HTML como export/import seguro, no como “modelo de verdad”.
- Definir la API del document model y sus invariantes.
- Comenzar Fase 0 con entorno, CI mínima y política segura de archivos.
- Preparar la primera iteración de tests: unidad + seguridad + integración mínima.

11. Nota final
-------------
La principal mejora respecto al plan original es que se incorpora seguridad, recuperación y rigor del producto como parte indispensable del diseño, no como una capa complementaria. Esto reduce riesgos técnicos y facilita la evolución del proyecto sin acumular deuda técnica.
