# Especificaciones de aceptación (specs) — Editor de texto tipo Word

1. Objetivo
-----------
Definir el comportamiento observable del editor para guiar el desarrollo mediante Spec-Driven Development (SDD). Este documento debe servir como contrato funcional, operativo y de seguridad para la primera versión del producto y para el crecimiento incremental del mismo.

El editor debe priorizar:
- fiabilidad y consistencia del documento
- seguridad por defecto
- testabilidad y trazabilidad
- compatibilidad mínima con HTML como formato de intercambio
- un modelo interno robusto y desacoplado de la capa de UI

2. Alcance y no alcance
-----------------------
2.1 Alcance del MVP
- Crear un documento nuevo
- Editar texto simple
- Aplicar formato básico (negrita, cursiva, subrayado)
- Cambiar tipo de letra y tamaño
- Ajustar alineación del párrafo
- Guardar documento en formato HTML seguro
- Abrir documento HTML seguro y validar integridad
- Recuperación básica ante cierre inesperado o fallo de guardado

2.2 No alcance del MVP
- editor de tablas avanzado
- edición WYSIWYG compleja de imágenes y layout
- sincronización en nube
- colaboración multiusuario
- importación/exportación avanzada de DOCX/ODT
- edición de documentos protegidos por contraseña
- ejecución de scripts o contenido activo en documentos importados

3. Principios de diseño
-----------------------
- El modelo de documento debe ser independiente de Qt y de la capa de UI.
- La serialización HTML debe ser estricta y segura, no un “dump” literal de un QDocument.
- La seguridad será una obligación funcional y no un extra opcional.
- Todo archivo abierto o importado debe validarse antes de ser procesado.
- El sistema debe soportar fallo controlado y recuperación, no pérdida silenciosa de contenido.

4. Requisitos no funcionales
----------------------------
4.1 Seguridad
- Todos los archivos importados deben validarse por tipo, tamaño y estructura.
- No se permitirá ejecución de scripts, `javascript:`, `data:` ni recursos remotos cargados desde documentos importados.
- Los SVG y otros formatos con capacidades de scripting deben rechazarse por defecto.
- Se debe bloquear la carga de contenido externo en HTML importado.
- Los documentos importados con estructura inválida deben rechazarse con error claro y sin corromper el documento actual.

4.2 Integridad y recuperación
- El guardado debe ser atómico: escribir a un archivo temporal y renombrarlo al finalizar correctamente.
- Debe existir recuperación de sesión tras cierre inesperado o fallo del proceso.
- El sistema debe evitar sobrescribir un archivo válido con contenido corrupto.
- Los archivos de recuperación temporales deben limpiarse en condiciones normales y mantenerse seguros.

4.3 Rendimiento y estabilidad
- El editor debe soportar documentos de tamaño razonable para uso personal sin degradación severa.
- La aplicación debe limitar imágenes y elementos por documento para evitar consumo excesivo de memoria.
- La lógica de edición debe poder ejecutarse en tests sin depender de UI para validación funcional.

5. Historias funcionales y criterios de aceptación
--------------------------------------------------
5.1 Historia: crear y editar texto básico
- Dado un documento nuevo, cuando el usuario escribe texto, entonces el texto se muestra en la vista y queda persistido cuando se guarda.
- Criterios de aceptación:
  1. El documento vacío se puede abrir y comenzar a editar en menos de 1 segundo en hardware de referencia.
  2. El texto introducido se conserva tras guardar y volver a abrir el documento.
  3. El documento debe soportar texto Unicode con caracteres latinos, acentos y símbolos básicos.
  4. Si el usuario intenta guardar con contenido no representable, el sistema debe mostrar un error claro y no perder el contenido actual.

5.2 Historia: formato básico (negrita, cursiva, subrayado)
- Dado un texto seleccionado, cuando el usuario aplica formato, entonces el estilo se aplica al rango seleccionado.
- Criterios de aceptación:
  1. Aplicar negrita, cursiva y subrayado sobre texto seleccionado debe producir un resultado visible en la UI.
  2. Al guardar y reabrir, el formato debe conservarse.
  3. Si no hay selección activa, el formato debe aplicarse al siguiente texto escrito.
  4. La aplicación debe soportar combinaciones de formato (ej: negrita + cursiva).

5.3 Historia: cambios de fuente y tamaño
- Dado un texto seleccionado o un cursor activo, cuando el usuario cambia la fuente o el tamaño, entonces el estilo se aplica al texto correspondiente.
- Criterios de aceptación:
  1. La fuente seleccionada obtiene efecto inmediato sobre el texto actual.
  2. La fuente y el tamaño se conservan en el documento serializado.
  3. Si la fuente solicitada no está disponible en el sistema, la aplicación debe caer a una fuente segura por defecto y no romper la edición.

5.4 Historia: alineación de párrafo
- Dado un bloque de texto o una posición de cursor, cuando el usuario cambia la alineación, entonces el párrafo se alinea según la opción elegida.
- Criterios de aceptación:
  1. Soporta izquierda, centrada, derecha y justificada.
  2. La alineación se conserva al guardar y reabrir.
  3. La alineación no afecta a otros párrafos no seleccionados.

5.5 Historia: guardar y abrir documento
- Dado un documento en edición, cuando el usuario guarda, entonces el sistema genera un archivo HTML seguro y válido.
- Criterios de aceptación:
  1. El archivo HTML generado debe ser válido, UTF-8 y sin scripts ni enlaces remotos no permitidos.
  2. El HTML debe incluir solo estilos inline permitidos y no referencias externas.
  3. Al abrir un archivo HTML válido generado por la aplicación, el documento debe mostrar el contenido y el formato esperados.
  4. Si el documento importado presenta etiquetas peligrosas o contenido malicioso, debe rechazarse con un mensaje de validación.

5.6 Historia: recuperación y guardado seguro
- Dado que el usuario está editando un documento, cuando ocurre un fallo o cierre inesperado, entonces el sistema debe conservar una versión recuperable.
- Criterios de aceptación:
  1. Se crea una copia temporal válida antes de guardar o reemplazar el documento actual.
  2. Tras un cierre inesperado, el usuario puede recuperar el último estado válido.
  3. La aplicación no debe destruir el documento original si el guardado final falla.

6. Requisitos de seguridad específicos
-------------------------------------
6.1 Entrada de archivos
- La importación de HTML, DOCX, ODT y archivos de imagen debe ejecutarse bajo una política de validación estricta.
- Se deben rechazar archivos mayores que el límite definido por producto y por plataforma.
- Las imágenes deben verificarse por MIME y por contenido real, no solo por extensión.
- Debe bloquearse cualquier imagen que no sea un raster seguro, salvo que se haya definido soporte explícito para SVG o formatos avanzados.

6.2 Sanitización de salida
- La salida HTML de la aplicación debe contar con sanitización y normalización antes de guardar.
- Deben evitarse etiquetas `script`, `iframe`, `object`, `embed`, `meta`, `link`, `style` con imports remotos, y URIs `javascript:`, `data:` o `vbscript:`.
- Los recursos externos deben eliminase o bloquearse en la salida.

6.3 Ficheros temporales
- Los archivos temporales deben estar en una zona privada y con permisos mínimos.
- Se debe garantizar limpieza de archivos temporales tras guardado correcto.
- No se debe escribir contenido temporal en ubicaciones accesibles por otros procesos no autorizados.

7. Pruebas de aceptación automatizables
----------------------------------------
7.1 Tests unitarios
- Serialización del documento interno a HTML seguro
- Aplicación de formato sobre rangos de texto
- Cambio de fuente y tamaño
- Gestión de alineaciones
- Validación de entrada de archivos
- Serialización y recuperación de documentos temporales

7.2 Tests de integración con pytest-qt
- Simular apertura de app en modo test
- Simular escritura de texto desde teclado
- Aplicar negrita, cursiva, subrayado y alineación desde toolbar
- Guardar y abrir documento HTML usando el flujo completo de UI
- Verificar que el documento reabierto coincide con el contenido esperado

7.3 Pruebas de seguridad
- HTML malicioso debe rechazarse
- SVG o contenido con scripts debe rechazarse
- Imágenes demasiado grandes deben rechazarse
- Documento corrupto debe fallar con un error manejado
- Intento de guardado en ruta inválida debe fallar sin borrar contenido previo

7.4 Pruebas de archivos
- Guardar un documento HTML válido y comparar contenido normalizado
- Abrir un archivo HTML generado por la aplicación y verificar que el contenido semántico coincide
- Validar que el archivo de salida no incluye scripts ni referencias externas no permitidas

8. Criterios de calidad
----------------------
- Cobertura mínima de unidad + integración para componentes críticos: documento, serialización, validación de archivos y recuperación.
- Formato de código aplicado (black, isort, flake8).
- CI ejecutando tests automáticamente en PRs.
- Revisión de seguridad en cada cambio que afecte a import/export, HTML o archivos.

9. Definición de hecho (Definition of Done)
-------------------------------------------
Para considerar una historia terminada:
- el código está en PR o rama funcional con tests que la cubren
- existe evidencia de validación funcional y de seguridad
- la documentación de uso mínimo está actualizada
- se han documentado los límites del soporte de formatos y archivos
- se han incluido pasos de QA manuales con casos peligrosos de archivo/HTML
- la historia no introduce regresiones en las historias ya aprobadas

10. Aceptación final
-------------------
El proyecto se considerará listo para una primera release cuando:
- el MVP esté completo
- la seguridad de import/export quede validada y documentada
- la recuperación de sesión y guardado seguro funcionen
- la exportación a PDF esté operativa
- haya pruebas automatizadas que cubran MVP y casos de seguridad clave
- la CI esté configurada y ejecutando validaciones en cada PR
- exista una guía de usuario básica, con advertencias de formatos y archivos no soportados

11. Cambios frente a la versión previa
--------------------------------------
- Se elimina la idea de que HTML sea “canónico” sin más restricciones.
- Se introduce un modelo interno estructurado que separa lógica de negocio y serialización.
- Se incorporan requisitos de seguridad y validación de entrada no negociables.
- Se refuerzan los criterios de aceptación con casos límite y condiciones explícitas.
- Se añaden requisitos de recuperación y robustez para evitar pérdida de trabajo.