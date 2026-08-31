# Tarea 005: Diseñar el modelo interno del documento

## Objetivo
Crear un modelo de documento independiente de la capa de presentación, que permita editar, serializar y validar el contenido de forma robusta y testeable.

## Subtareas
- Definir la entidad `Documento`.
- Diseñar bloques, texto, estilo, metadatos y atributos.
- Separar la lógica del documento de la lógica visual.
- Establecer invariantes y reglas del modelo.

## Tareas a realizar
1. Definir la estructura del documento en memoria.
2. Establecer cómo se representan texto, párrafos y estilos.
3. Crear la API mínima para mutar el contenido.
4. Asegurar que el modelo se pueda probar sin UI.

## Criterios de aceptación
- El modelo es independiente de Qt y de la capa UI.
- Se puede crear, editar y serializar un documento sin depender de la vista.
- La lógica del negocio está separada claramente de la interfaz.

## Pruebas de aceptación
- Crear un documento vacío y verificar que es válido.
- Insertar texto Unicode y comprobar que se conserva.
- Aplicar estilo a una sección y validar que la estructura interna cambia correctamente.
