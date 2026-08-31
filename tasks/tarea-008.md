# Tarea 008: Implementar pruebas unitarias del modelo

## Objetivo
Cubrir con pruebas automatizadas la lógica interna del documento para evitar regresiones y validar la base funcional del editor.

## Subtareas
- Crear pruebas para creación de documento vacío.
- Probar inserción de texto Unicode.
- Probar formato básico sobre rangos.
- Verificar cambio de fuente, tamaño y alineación.
- Comprobar serialización básica a HTML.

## Tareas a realizar
1. Diseñar tests unitarios para cada operación crítica.
2. Ejecutar los tests en la capa de negocio sin UI.
3. Validar que los resultados son deterministas.
4. Corregir cualquier regresión funcional detectada.

## Criterios de aceptación
- La lógica principal del documento queda cubierta por pruebas automatizadas.
- Los requisitos fundamentales del MVP tienen evidencia técnica.
- Las pruebas sirven como referencia para cambios futuros.

## Pruebas de aceptación
- Ejecutar la suite unitaria del modelo.
- Confirmar que todas las pruebas pasan.
- Verificar que un cambio incorrecto en el estilo o la serialización se detecta como fallo.
