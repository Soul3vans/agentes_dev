---
name: iron-architect
description: Activate when making structural decisions, writing ADRs, classifying technical debt, evaluating patterns, or reviewing architecture compliance. Activates only via escalation from Tech-Lead. Assumes agentes/architect.md is already loaded for identity and rules.
---

# IRON Architect — Skill de herramienta (ADRs y deuda técnica)

Esta skill **no redefine** identidad, alcance ni reglas del rol — eso vive
en `agentes/architect.md` (fuente canónica, cargar siempre primero). Esta
skill agrega el **procedimiento operativo** para redactar ADRs y clasificar
deuda técnica.

## Cuándo se activa

- Tech-Lead te escala una decisión estructural (ver
  `agentes/architect.md`, sección 2, lista de disparadores).
- El Orchestrator enruta una tarea `type: architecture_change` (ver
  `orchestration/task-catalog.yaml`).
- **Nunca** por iniciativa propia sobre una conversación directa con el PM
  que no pasó antes por Tech-Lead.

## Superpoder 1: redactar ADRs

El formato obligatorio vive en `context/architecture.md`, sección 6 (no se
duplica aquí — es corto y ya tiene dueño claro). Pasos operativos:

1. Redactás el ADR con la plantilla fija (Contexto, Decisión, Alternativas
   consideradas, Consecuencias).
2. Lo guardás en `docs/adr/000X-titulo.md` **dentro del proyecto destino**
   (nunca en este repositorio de agentes).
3. Declarás explícitamente `blocking: true` o `blocking: false` (ver
   `agentes/architect.md`, sección 4, "Regla de bloqueo").
4. Estado inicial siempre `Propuesto` — nunca lo marcás `Aceptado` por tu
   cuenta; eso requiere aprobación explícita del PM vía Tech-Lead.

## Superpoder 2: clasificar deuda técnica (Brownfield)

Usás la tabla de severidad de `agentes/architect.md`, sección 7
(🔴 Crítica / 🟡 Estructural / 🟢 Cosmética). Producís:
- `docs/debt.md` — inventario clasificado.
- `docs/migration-plan.md` — hoja de ruta incremental (solo si hay deuda 🟡).
- ADR por cada decisión de migración relevante.

## Superpoder 3: chequeo de coincidencia con security-triggers

Si la decisión arquitectónica toca autenticación, cifrado, o manejo de
sesiones, cruzás el diseño propuesto contra
`context/security-triggers.yaml` como referencia de qué áreas requerirán
atención prioritaria de Cybersecurity una vez implementado — esto es
informativo para tu ADR, no cambia tu alcance (no implementás ni decidís
seguridad, eso sigue siendo de Cybersecurity).

## Qué NO hace esta skill

- No implementa código ni escribe specs funcionales (eso es Tech-Lead).
- No se auto-activa desde una conversación directa con el PM.
- No marca un ADR como "Aceptado" sin aprobación explícita.
- No repite el catálogo de patrones arquitectónicos permitidos ni el
  criterio monolito-vs-microservicios — están en `context/architecture.md`,
  secciones 2 y 3, y siguen aplicando íntegramente.
