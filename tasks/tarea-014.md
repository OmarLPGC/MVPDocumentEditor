# Tarea 014: Añadir cambio de fuente y tamaño

## Objetivo
Permitir al usuario controlar la tipografía y el tamaño del texto, con una estrategia segura cuando la fuente elegida no está disponible.

## Subtareas
- Definir la lista de fuentes compatibles con el editor.
- Añadir la operación de cambio de fuente en el modelo.
- Añadir el cambio de tamaño de texto.
- Definir fallback a una fuente segura si la solicitada no existe.

## Tareas a realizar
1. Implementar el estilo de fuente y tamaño en la API del documento.
2. Conectar el control gráfico correspondiente.
3. Añadir comportamiento seguro cuando una fuente no esté instalada.
4. Validar que el estilo se serializa correctamente.

## Criterios de aceptación
- La fuente y el tamaño se aplican al texto actual.
- El estilo se mantiene al guardar y reabrir el documento.
- Si la fuente no está disponible, se usa una alternativa segura y no se rompe la edición.

## Pruebas de aceptación
- Cambiar la fuente a una disponible y comprobar el resultado visual.
- Cambiar el tamaño y guardar para validar la persistencia.
- Probar una fuente inexistente y confirmar fallback correcto.
