# Seguridad del Control Plane

- El Action sigue separado del access key del panel.
- Los planes tienen máximo ocho pasos.
- Cada tool valida su input y nivel de riesgo.
- `publish`, `rollback` y operaciones destructivas requieren `confirmed: true`.
- Los patches bloquean claves de prototype pollution, HTML directo, profundidad y tamaño excesivos.
- Las publicaciones se encolan; el GPT no obtiene acceso a GitHub, Railway ni secretos.
- `request_id` evita duplicar publicaciones.
- Los eventos de ejecución se guardan sin secretos completos.

La instalación sigue siendo de propietario único. Si más adelante se comparte el GPT, se debe sustituir la clave estática por identidad por usuario antes de habilitar operaciones de escritura.
