# Tarea 013: Implementar formato básico sobre texto seleccionado

## Objetivo
Añadir las herramientas básicas de formato al editor: negrita, cursiva y subrayado, aplicables a una selección o al texto que se escriba a continuación.

## Subtareas
- Definir cómo se representarán los estilos en el modelo.
- Conectar acciones de toolbar con las propiedades de estilo.
- Aplicar el estilo al rango seleccionado.
- Habilitar el formato para el próximo texto escrito cuando no exista selección.

## Tareas a realizar
1. Implementar el modelo de estilos básicos.
2. Conectar la UI con el formato de documento.
3. Comprobar que los estilos se aplican correctamente a los rangos.
4. Asegurar que el formato se conserva al guardar.

## Criterios de aceptación
- La negrita, cursiva y subrayado son visibles en la UI.
- El estilo se conserva en el documento serializado.
- El usuario puede aplicar formato a un rango o al texto posterior.

## Pruebas de aceptación
- Seleccionar una parte del texto y aplicar estilo.
- Compruebar que el cambio es visible.
- Guardar y reabrir para validar que el formato persiste.
