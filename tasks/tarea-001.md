# Tarea 001: Preparar la estructura del repositorio

## Objetivo
Crear la base del proyecto para que el desarrollo del editor de texto siga una organización clara, mantenible y testeable desde el primer momento.

## Subtareas
- Definir la estructura de carpetas del proyecto: `src`, `tests`, `docs`, `assets`, `scripts` y configuraciones.
- Establecer la separación entre lógica de negocio, serialización, validación, almacenamiento y capa de UI.
- Crear una convención de nombres para módulos, clases y pruebas.
- Preparar el repositorio para una evolución incremental sin acoplar lógica de negocio con Qt o con la interfaz.

## Tareas a realizar
1. Crear la jerarquía básica de carpetas.
2. Redactar la estructura de archivos propuesta para cada capa del sistema.
3. Establecer reglas de organización para tests y documentación.
4. Asegurar que cada componente tenga un propósito claro y sin solapamientos.

## Criterios de aceptación
- El repositorio tiene una estructura clara y reutilizable.
- Cada capa del sistema tiene una ubicación definida.
- El proyecto permite crecer sin mezclar responsabilidades.

## Pruebas de aceptación
- Verificar que la estructura principal existe y es consistente.
- Comprobar que los módulos no tienen dependencias directas indebidas con la capa GUI.
- Confirmar que la organización de archivos facilita el desarrollo y la revisión.
