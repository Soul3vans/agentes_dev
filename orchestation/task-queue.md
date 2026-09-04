# Diseño de cola de tareas y workers idempotentes

> **Estado: DISEÑO FUTURO**  
> Este documento describe una visión de escalado.  
> **No forma parte del runtime actual** de IRON (1 modelo, ejecución secuencial).  
> El Orchestrator y los agentes **no deben cargarlo ni asumir** que las capacidades aquí descritas están disponibles.  
> Activación: solo cuando se migre formalmente a multi-worker / CI automatizada / API de nion-cli.

Objetivo: introducir una cola de tareas robusta (RabbitMQ / Redis Streams) con garantías de entrega, deduplicación y visibility timeout.

1. Elección de tecnología
- Redis Streams: simple, buen rendimiento, soporta consumer groups.
- RabbitMQ: modelos avanzados de routing/exchanges y prioridad nativa.

2. Modelo de mensajes
- Payload mínimo:
  - `task_id` (UUID)
  - `type` (feature, bug, etc.)
  - `spec_ref` (ruta a spec)
  - `resource_scope`
  - `payload` (metadatos)
  - `attempts`

3. Entrega y visibilidad
- Consumer groups + ack: worker consume -> process -> ack.
- Si worker falla o crash, message queda pendiente y otro consumer lo procesa.
- Implementar `max_attempts` y mover a `dead_letter_queue` si excede.

4. Deduplicación
- Antes de encolar, Orchestrator verifica si `task_id` ya existe en store (Redis set) → evita duplicados.

5. Idempotencia
- Workers deben ser idempotentes: verificar si `task_id` ya fue completada (persistir estado final) antes de aplicar efectos.
- Diseñar operaciones reversibles o con claves de idempotencia para APIs externas.

6. Retries y backoff
- Exponential backoff entre reintentos.
- Estrategia: inmediato (1), corto (2), largo (3), dead-letter.

7. Observabilidad
- Métricas: `queue_depth`, `consumer_lag`, `dlq_count`, `processing_rate`.
- Tracing: propagar `task_id` y `trace_id`.

8. Respaldo y operaciones
- Snapshot de streams (si Redis) y monitorización del lag.
- Procedimientos de reingestión desde DLQ con validación humana.
