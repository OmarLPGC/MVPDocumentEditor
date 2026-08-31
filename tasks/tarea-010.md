# Tarea 010: Implementar la edición de texto básica

## Objetivo
Permitir al usuario escribir, borrar y seleccionar texto dentro del documento, de forma coherente con la interfaz y con la lógica del modelo.

## Subtareas
- Conectar teclado y entrada de texto con el documento activo.
- Permitir texto Unicode con acentos y símbolos básicos.
- Soportar cursor, selección y borrado básico.
- Gestionar el estado de edición visible en la UI.

## Tareas a realizar
1. Integrar la edición con la vista principal.
2. Garantizar la entrada correcta de texto desde teclado.
3. Verificar que los caracteres especiales no rompen la serialización.
4. Comprobar selección y edición del contenido actual.

## Criterios de aceptación
- El usuario puede escribir y ver el texto de inmediato.
- El comportamiento del cursor y de la selección es estable.
- El texto se conserva en memoria y al guardar.

## Pruebas de aceptación
- Escribir una frase con acentos y símbolos.
- Borrar partes del texto y comprobar que el contenido cambia correctamente.
- Verificar que el documento mantiene la estructura del texto tras varios cambios.
