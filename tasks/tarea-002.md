# Tarea 002: Definir entorno de desarrollo y calidad

## Objetivo
Preparar un entorno reproducible para desarrollar, probar y validar el editor con estándares mínimos de calidad y automatización.

## Subtareas
- Configurar Python 3.10+ y entorno virtual o Poetry.
- Definir dependencias principales: PySide6, pytest, pytest-qt, Pillow, black, isort, flake8.
- Crear configuración mínima para formateo y lint.
- Preparar una pipeline de CI con ejecución automática de tests.

## Tareas a realizar
1. Inicializar el entorno de desarrollo.
2. Registrar dependencias en la configuración del proyecto.
3. Añadir reglas de formateo y calidad.
4. Configurar CI para lanzar las pruebas en cada cambio.

## Criterios de aceptación
- El entorno puede reinstalarse fácilmente en una máquina nueva.
- La aplicación y los tests se ejecutan sin errores de dependencias.
- La CI valida automáticamente la calidad y la funcionalidad básica.

## Pruebas de aceptación
- Ejecutar la instalación de dependencias desde cero.
- Ejecutar `pytest` sin errores iniciales.
- Verificar que la CI se activa correctamente en un cambio de código.
