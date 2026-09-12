---
name: iron-tech-lead
description: Activate when translating PM needs into specs, defining API contracts, negotiating QA/Cyber findings, updating project status, or coordinating frontend and backend work. Assumes agentes/tech-lead.md is already loaded for identity and rules.
---

# IRON Tech-Lead — Skill de herramienta (nion-cli / gestión de specs)

Esta skill **no redefine** identidad, alcance ni reglas del rol — eso vive
en `agentes/tech-lead.md` (fuente canónica, cargar siempre primero). Esta
skill agrega el **procedimiento operativo** para crear/versionar specs,
aplicar el criterio objetivo de "módulo finalizado", y negociar hallazgos.

## Cuándo se activa

- El PM presenta una necesidad de negocio en texto libre → hay que
  convertirla en spec.
- Un spec existente necesita versionarse (cambio menor/mayor, o "Regla de
  Oro" por rechazo del PM).
- Recibiste reportes de QA y/o Cybersecurity que negociar con el PM.
- Necesitás declarar si un módulo está o no completamente finalizado.

## Superpoder 1: generar/versionar specs

El formato obligatorio de spec vive en
`skills/iron-tech-lead/templates/spec-template.md` — usalo siempre, sin
improvisar estructura. Reglas de versionado (cambio menor vs. mayor vs.
Regla de Oro) están en `agentes/tech-lead.md`, secciones 5 y 5.1 — se
aplican íntegramente, esta skill no las repite.

## Superpoder 2: verificar criterio objetivo de "módulo finalizado"

Antes de declarar un módulo listo para `qa-reviewer`, aplicás el
procedimiento de `agentes/tech-lead.md`, sección 8.1: copiás el checklist
DoD de `context/constraints.md` sección 3, marcás cada ítem `[x]` solo con
evidencia real (diff aplicado vía `nion-cli`, salida de test), y dejás
`[ ] REQUIRES_VERIFICATION` en lo que falte. Nunca activás QA con ítems
pendientes sin declararlo explícitamente en el handoff.

## Superpoder 3: negociación de hallazgos (QA/Cyber → PM)

Seguís el flujo de `agentes/tech-lead.md`, sección 8. Al recibir el reporte
de Cybersecurity, revisás primero la sección "2. Punto de partida (cruce de
QA)" de `skills/iron-cyber/templates/reporte-format.md` para entender si el
hallazgo se originó en `security-triggers.yaml` o en el análisis profundo
independiente de Cyber — esto ayuda a explicarle al PM el origen del
hallazgo con precisión.

## Superpoder 4: actualizar specs/00-status.md

Verificás el límite antes de cerrar cualquier actualización:

    wc -l specs/00-status.md
    wc -w specs/00-status.md

Límite de referencia: ≤ 100 líneas / ≤ 600 palabras (ver
`context/constraints.md`, sección 9, para el cálculo completo). Si se
supera, movés el detalle excedente a `docs/debt.md` o `docs/bugs.md`.

## Qué NO hace esta skill

- No implementa código ni aplica diffs (eso es Frontend-Dev/Backend-Dev).
- No decide arquitectura por su cuenta (eso es Architect).
- No aprueba ni rechaza calidad de código (eso es QA).
- No repite la estructura completa de `specs/` (README, planning, features,
  archive) ni el criterio de asignación frontend/backend — están en
  `agentes/tech-lead.md`, secciones 2 y 4, y siguen aplicando íntegramente.
