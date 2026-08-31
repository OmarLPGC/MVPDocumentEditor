# Tarea 012: Desarrollar pruebas de integración de la interfaz

## Objetivo
Validar que el flujo completo de la GUI, desde la edición hasta el guardado y la reapertura, funciona de manera coherente en la práctica.

## Subtareas
- Simular apertura de la aplicación en modo test.
- Insertar texto desde la UI.
- Guardar el documento y abrirlo de nuevo.
- Verificar que el contenido y el formato coinciden con la expectativa.

## Tareas a realizar
1. Preparar tests de integración con `pytest-qt`.
2. Simular la interacción real con la ventana.
3. Validar la persistencia del contenido a través del flujo completo.
4. Comprobar que los resultados no dependen de la lógica interna únicamente.

## Criterios de aceptación
- La UI puede ser probada sin intervención manual.
- El flujo completo de edición, guardado y apertura funciona estabilmente.
- Los resultados de integración están alineados con la especificación.

## Pruebas de aceptación
- Escribir contenido en la app y guardar.
- Reabrir el documento y confirmar que coincide con el texto introducido.
- Verificar que el comportamiento visual y funcional corresponde al requisito funcional.
