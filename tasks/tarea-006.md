# Tarea 006: Crear la API de edición del documento

## Objetivo
Implementar la API que permita manipular el contenido del documento desde la lógica de negocio y desde pruebas unitarias y de integración.

## Subtareas
- Añadir funciones para insertar texto.
- Añadir rangos y selección.
- Definir operaciones para aplicar formato.
- Definir operaciones para cambiar fuente, tamaño y alineación.

## Tareas a realizar
1. Diseñar métodos para insertar y modificar texto.
2. Añadir soporte para selección y cursor de edición.
3. Incorporar formato básico sobre rangos de texto.
4. Establecer validaciones mínimas de integridad del documento.

## Criterios de aceptación
- La API permite editar el documento de forma programática.
- Los cambios quedan consistentes en el modelo.
- Se pueden ejecutar pruebas sin ninguna dependencias visuales.

## Pruebas de aceptación
- Insertar texto y comprobar que el documento mantiene orden y contenido.
- Aplicar negrita y cursiva sobre un rango y verificar que la representación interna refleja el cambio.
- Cambiar alineación de un párrafo y asegurar que solo afecta al bloque deseado.
