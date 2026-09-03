# Concurrencia configurable y pool de workers

Objetivo: permitir pasar de un modelo secuencial (1) a un pool de workers concurrentes, manteniendo seguridad, locking por recurso y garantías de idempotencia.

1. Principios
- Concurrency configurable: parámetro `MAX_WORKERS` en la orquestación.
- Locking por recurso/escope: cada spec define `resource_scope` (p.ej. `module:users`, `db:migrations`).
- Leasing y timeouts: locks con TTL para evitar deadlocks si un worker muere.
- Workers idempotentes: cada task incluye `task_id` y se procesa con semántica idempotente.

2. Arquitectura propuesta
- Orchestrator pone tareas en la cola con `resource_scope` y `task_id`.
- Workers registran heartbeat y adquieren lock (Redis RedLock o similar) por `resource_scope` antes de procesar.
- Si lock adquirido: procesar; al terminar liberar lock y marcar task completed.
- Si lock no disponible: replanificar con backoff o procesar otras tareas.

3. Locking detallado
- Implementar locks distribuidos (Redis RedLock o ZooKeeper) con TTL y renew.
- Locks por nivel: `resource_scope` granular (tabla, servicio) y `global` para tareas críticas (migrations).
- Evitar holding long-running locks: separar pasos de trabajo en subtasks que puedan liberar locks entre pasos.

4. Configuración
- `MAX_WORKERS` (default 1)
- `LOCK_BACKEND` (redis|zookeeper)
- `LOCK_TTL` (segundos)
- `WORKER_HEARTBEAT` (segundos)

5. Estrategias de fairness
- Prioridad por `risk_level` (high/medium/low) con cola prioritaria
- Aging: tareas que esperan demasiado suben de prioridad

6. Observabilidad
- Métricas: `worker_count`, `tasks_in_flight`, `lock_acquire_rate`, `lock_wait_time`, `task_latency`.
- Tracing: correlar `task_id` con traces distribuidos (OpenTelemetry).

7. Recomendación
- Empezar con `MAX_WORKERS=2` y pruebas de integración; validar invariantes (no dos workers con el mismo `resource_scope`).
