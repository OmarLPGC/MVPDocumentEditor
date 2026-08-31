# Tarea 004: Preparar la primera batería de pruebas base

## Objetivo
Iniciar la validación automatizada con pruebas mínimas que cubran los requisitos esenciales del producto antes de implementar la lógica completa.

## Subtareas
- Crear tests para serialización básica del documento.
- Crear tests para validación de HTML importado.
- Crear tests para guardado y lectura simple de contenido.
- Añadir casos de seguridad iniciales.

## Tareas a realizar
1. Diseñar los tests mínimos para cada capa crítica.
2. Asegurar que los tests pueden ejecutarse sin una UI completa.
3. Preparar pruebas deterministas para contenido seguro y contenido malicioso.
4. Revisar que los tests cubran los requisitos funcionales esenciales.

## Criterios de aceptación
- Existe una batería base de tests ejecutable.
- Los tests fallan si la lógica no cumple requisitos clave.
- La base de pruebas sirve como contrato para el desarrollo incremental.

## Pruebas de aceptación
- Ejecutar el conjunto base de pruebas con `pytest`.
- Confirmar que se detectan fallos en serialización y validación.
- Verificar que la suite se usa como referencia para el desarrollo futuro.
