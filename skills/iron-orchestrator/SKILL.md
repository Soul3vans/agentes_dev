---
name: iron-orchestrator
description: Activate when classifying a new PM request, deciding which agent to call, enforcing workflow order, or starting any IRON multi-agent task. Assumes agentes/orchestrator.md is already loaded for identity and rules.
---

# IRON Orchestrator — Skill de herramienta (clasificación y enrutamiento)

Esta skill **no redefine** identidad ni autoridad del rol — eso vive en
`agentes/orchestrator.md` (fuente canónica, cargar siempre primero). Esta
skill agrega el **procedimiento operativo** para clasificar solicitudes y
generar el reporte de enrutamiento.

## Cuándo se activa

- Cada vez que el PM presenta una solicitud nueva, antes de delegar a
  cualquier agente técnico.

## Superpoder: clasificación contra el catálogo

1. Leés `orchestration/task-catalog.yaml` (y el override del proyecto, si
   existe).
2. Leés `specs/00-status.md` si existe.
3. Clasificás la solicitud contra los `type` del catálogo.
4. Verificás si la entrada tiene `security_check` (ver
   `orchestration/task-catalog.yaml`, entradas `feature` y `bug`) y lo
   incluís en tu reporte si aplica.
5. Emitís el reporte con el formato obligatorio de
   `agentes/orchestrator.md`, sección 7 — **incluyendo siempre el campo
   `Iteración: N/10`**, con la regla de conteo/reinicio descrita ahí mismo.

## Formato de reporte (referencia rápida)

    [ORCHESTRATOR]
    Tarea detectada: <type del catálogo>
    Agente asignado: <handler>
    Escenario: <A / B / N/A>
    Archivos de contexto cargados: <lista mínima>
    Chequeo de seguridad aplicable: <security_check del catálogo, si existe>
    Escalación aplicada (si corresponde): <de → a>
    Iteración: <N>/10
    ¿Procedo? (sí/no/ajustar)

No existe `templates/` separado — el formato es corto y ya vive completo en
`agentes/orchestrator.md` sección 7; esta skill solo lo referencia como
recordatorio operativo rápido.

## Qué NO hace esta skill

- No decide contenido técnico ni alcance de negocio.
- No inventa tipos de tarea fuera del catálogo.
- No carga el proyecto completo — solo lo estrictamente necesario para
  clasificar.
- No repite la mecánica de escalación automática vs. manual — está en
  `agentes/orchestrator.md`, sección 5, y sigue aplicando íntegramente.
