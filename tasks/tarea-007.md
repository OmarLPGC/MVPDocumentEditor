# Tarea 007: Diseñar la serialización segura a HTML

## Objetivo
Definir el mecanismo de exportación del documento a HTML seguro, validado y compatible con el intercambio mínimo requerido por el producto.

## Subtareas
- Crear un serializador para transformar el modelo interno en HTML.
- Normalizar estilos permitidos.
- Eliminar etiquetas y atributos peligrosos.
- Asegurar UTF-8 y limpieza de contenido activo.

## Tareas a realizar
1. Diseñar la salida HTML segura del documento.
2. Filtrar contenido no permitido.
3. Garantizar que no se exporten scripts, enlaces remotos ni URLs maliciosas.
4. Validar la salidas HTML con pruebas unitarias.

## Criterios de aceptación
- El HTML generado es válido, seguro y uniforme.
- Se elimina contenido peligroso.
- La serialización se puede probar y reproducir.

## Pruebas de aceptación
- Generar un documento con formato y comprobar que el HTML incluye solo estilos permitidos.
- Verificar que no hay etiquetas `script`, `iframe`, `object` o recursos externos.
- Comprobar que el contenido Unicode se escribe correctamente en UTF-8.
