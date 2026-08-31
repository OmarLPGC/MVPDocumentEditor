# Tarea 011: Implementar el flujo de guardar y abrir documento

## Objetivo
Crear la funcionalidad esencial de persistencia para que el usuario pueda guardar el documento actual y abrirlo posteriormente con validación de seguridad.

## Subtareas
- Añadir acciones de guardar y abrir.
- Serializar el documento a HTML seguro.
- Guardar con codificación UTF-8.
- Validar el archivo antes de abrirlo.
- Mostrar errores claros en caso de documento inválido.

## Tareas a realizar
1. Integrar el guardado desde la UI.
2. Generar un archivo HTML seguro y válido.
3. Recuperar el contenido desde un archivo HTML autorizado.
4. Validar errores y mensajes de usuario.

## Criterios de aceptación
- La app puede guardar un documento y abrirlo de nuevo.
- El archivo generado es HTML válido y seguro.
- Los documentos no válidos se rechazan sin corromper el documento actual.

## Pruebas de aceptación
- Guardar un documento con texto y formato básico.
- Cerrar y reabrir el archivo.
- Intentar abrir un archivo HTML malicioso y comprobar que se bloquea.
