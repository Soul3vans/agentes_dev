# RBAC y Observabilidad (diseño)

Objetivo: formalizar roles y permisos y definir métricas/observabilidad necesarias para escalar.

1. Roles y permisos (ejemplo)
- `PM`:
  - puede aprobar diffs, decidir sobre hallazgos, activar deploys canary
- `Tech-Lead`:
  - crear/specs, asignar tareas, solicitar escalación a `Architect`
- `Developer` (frontend/backend):
  - proponer diffs, ejecutar verifications localmente
- `QA-Reviewer`:
  - aprobar/rechazar PRs, ejecutar suites de integración
- `Architect` / `Cybersecurity`:
  - evaluar ADRs / auditorías (read + comment); pueden marcar `blocking`
- `Orchestrator` (system role):
  - crear tareas en la cola, actualizar estados, no aplica código

2. Permisos mínimos por endpoint (nion-cli API)
- `POST /apply`: PM, Tech-Lead (require approval workflow)
- `POST /verify`: CI service, Devs (scoped)
- `POST /rollback`: PM, Tech-Lead
- `GET /evidence`: all roles read but only PM/Tech-Lead can request full artifacts

3. Auditoría y trazabilidad
- Registrar quién solicitó, quién aprobó, cuándo, evidencia de ejecución (artefacto link).
- Almacenar artefactos en storage inmutable con path `evidence/{task_id}/{run_id}`.

4. Métricas y dashboards recomendados
- Task throughput (tasks/sec)
- Task latency (enqueue -> complete)
- Worker concurrency (active workers)
- Queue depth and DLQ size
- Lock wait times and lock contention
- Canary metrics: error rate, p95 latency, saturation
- CI pass rate and evidence attach rate

5. Tracing y logs
- Propagar `task_id` y `trace_id` en logs and traces
- Exponer traces via OpenTelemetry and visualizar en Jaeger/Tempo
- Logs estructurados en JSON y enviados a ELK/Datadog

6. Alerting
- Alert on: high DLQ growth, worker crash spikes, canary error rate > threshold, lock deadlocks

7. Recomendación de rollout
- Implementar RBAC centralizado (AuthZ service) y sincronizar con CI users and PM accounts.
- Inicialmente, usar a simple mapping (GitHub org teams → roles) y luego migrar a granular claims in JWT.
