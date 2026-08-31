# Tarea 003: Definir la política inicial de seguridad para archivos

## Objetivo
Establecer las reglas de seguridad para la importación y exportación de archivos, evitando la apertura de contenido malicioso o no soportado.

## Subtareas
- Definir límites de tamaño por tipo de archivo.
- Definir extensiones y tipos MIME permitidos.
- Rechazar scripts, `javascript:`, `data:`, SVG y recursos externos en documentos importados.
- Establecer un flujo de validación para HTML y archivos de imagen.

## Tareas a realizar
1. Crear una política de validación de entrada.
2. Definir reglas para archivos HTML, imágenes y otros formatos soportados.
3. Determinar qué tipos de contenidos se rechazan por defecto.
4. Registrar la política en la documentación técnica.

## Criterios de aceptación
- Todo archivo importado se valida antes de procesarse.
- Los archivos con contenido activo o malicioso son rechazados.
- La app no ejecuta scripts ni recursos externos desde documentos abiertos.

## Pruebas de aceptación
- Importar un HTML con script y comprobar que es bloqueado.
- Probar un SVG con contenido activo y verificar que se rechaza.
- Validar que una imagen demasiado grande queda bloqueada.
