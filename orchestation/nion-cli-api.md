# nion-cli: API y webhooks (diseño)

Objetivo: convertir `nion-cli` en un agente de ejecución automatizable con API y webhooks para integrarlo en CI/CD y orquestación.

1. Principales endpoints (REST)
- `POST /apply` — aplicar un diff
  - body: `{ pr_number, diff, author, reason, verification_commands: [] }`
  - response: `{ task_id, status }`
- `POST /verify` — ejecutar comandos de verificación (tests, linters)
  - body: `{ task_id, commands[] }`
  - response: `{ run_id, status }`
- `GET /status/{task_id}` — obtener estado y evidencia
- `POST /rollback` — aplicar rollback por `task_id` o `tag`
- `GET /evidence/{run_id}` — descargar stdout/stderr y artefactos

2. Webhooks (events)
- `nion.apply.started` `{ task_id, pr_number }`
- `nion.apply.completed` `{ task_id, status, evidence_ref }`
- `nion.verify.completed` `{ run_id, status, evidence_ref }`
- `nion.rollback.completed` `{ task_id, status }`

3. Seguridad
- Autenticación: token JWT con claims: `role`, `actor_id`.
- Autorización: verificar que el actor puede solicitar `apply` (PM/Tech-Lead) o `verify` (CI/system).
- Rate limits y auditoría de acciones.

4. Integración con CI
- CI lanza `POST /verify` con comandos a ejecutar; `nion` ejecuta y sube evidencia.
- Para `apply`, PM aprueba en UI; CI/Orchestrator invoca `POST /apply` con el diff y escucha webhooks para resultados.

5. Recomendaciones de implementación
- Hacer la API idempotente: `task_id` deduplica solicitudes.
- Registrar todo en almacenamiento inmutable (S3/artifacts) para evidencia KNOWN.
- Firmar webhooks y permitir reintentos.

6. Ejemplo de payload `POST /apply`

```json
{
  "pr_number": 123,
  "diff": "--- a/file\n+++ b/file\n...",
  "author": "backend-dev",
  "reason": "Fixes bug X",
  "verification_commands": ["npm test", "npm run lint"]
}
```
