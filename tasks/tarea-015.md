# Tarea 015: Implementar alineación de párrafos

## Objetivo
Añadir soporte para la alineación izquierda, centrada, derecha y justificada, para que cada bloque de texto pueda ajustarse adecuadamente.

## Subtareas
- Definir la API de alineación en el modelo.
- Conectar las opciones de alineación en la UI.
- Asegurar que el cambio afecta solo al bloque seleccionado o al párrafo activo.
- Garantizar la persistencia de la alineación.

## Tareas a realizar
1. Definir los valores de alineación válidos.
2. Conectar la acción con el documento.
3. Validar que no afecta a otros bloques.
4. Verificar que se conserva al guardar y reabrir.

## Criterios de aceptación
- Las cuatro alineaciones están implementadas.
- La alineación no afecta a otros párrafos.
- La alineación persiste en la salida serializada.

## Pruebas de aceptación
- Alinear un párrafo a la derecha y comprobar la vista.
- Aplicar alineación centrada y confirmar no afecta a otros bloques.
- Guardar y reabrir para verificar la persistencia.
