# Política inicial de seguridad para archivos

La aplicación valida cualquier archivo antes de incorporarlo al modelo del
documento. La validación se realiza por extensión permitida, tamaño, estructura
y contenido real; la extensión por sí sola no es suficiente.

## HTML

- Se aceptan únicamente `.html` y `.htm`.
- El límite inicial es de 5 MiB.
- El contenido debe estar codificado en UTF-8.
- Se rechazan `script`, `iframe`, `object`, `embed`, `meta`, `link` y `style`.
- Se rechazan atributos de eventos (`onclick`, `onload`, etc.).
- Se rechazan URLs `javascript:`, `data:`, `vbscript:`, HTTP, HTTPS y FTP.
- No se permiten recursos externos ni formularios que envíen datos.

## Imágenes

- Se aceptan únicamente PNG, JPEG, GIF, BMP y WEBP rasterizados.
- SVG se rechaza por defecto porque puede contener contenido activo.
- El límite inicial es de 10 MiB y 40 millones de píxeles.
- Se comprueba la firma y la estructura básica del contenido; no se confía
  únicamente en la extensión.

## Tipos no permitidos

Los tipos no incluidos explícitamente en la política se rechazan. Esto incluye
formatos con macros o contenido ejecutable como DOCM, EXE y similares. La
compatibilidad con DOCX u ODT deberá definir validadores específicos antes de
habilitarse.

## Manejo de errores

Un archivo rechazado genera `FileValidationError`. El consumidor debe mostrar un
mensaje claro y conservar intacto el documento que ya estaba abierto.
