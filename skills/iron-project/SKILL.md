---
name: iron-project
description: Activate when you need to know what operations already exist for managing project workspaces (create/clone/switch/map) or which test runners are available for QA/Cybersecurity's Carril B. Router only — the real logic lives in iron_ops/ and orchestration/test-runners.yaml, never duplicated here.
---

# IRON Project — Skill de referencia (Project Service)

Esta skill es un **router**, no un contenedor de lógica. Le dice a cualquier
agente (Architect, Tech-Lead, QA-Reviewer, Cybersecurity) qué operaciones ya
existen antes de que proponga un comando manual (`ls`, `find`, `git clone` a
mano, etc.) — reforzando el protocolo anti-alucinación de
`context/constraints.md`, sección 10.

## Qué existe ya (no lo reinventes)

- **Crear/clonar/cambiar de proyecto activo**: `iron-ops crear|clonar|ir`
  (ver `iron_ops/project_service.py`). Sin confirmación humana — Carril A
  (`orchestration/task-catalog.yaml`, types `project_create`/`project_clone`/
  `project_switch`).
- **Mapa del proyecto**: `iron-ops mapa` genera
  `.iron_mapa/mapa_completo.json` dentro del proyecto activo (ver
  `iron_ops/project_mapper.py`) — estructura, hash, y para cada archivo sus
  imports/clases/funciones principales según el lenguaje. Antes de proponer
  un comando de verificación manual (`find`, `grep -r`, etc.) para saber qué
  archivos o funciones existen, consultá primero si este mapa ya tiene la
  respuesta.
- **Ejecutar un test nuevo** (exclusivo de `qa-reviewer`/`cybersecurity`): la
  Action `{stack, target_path, flags}` se valida contra
  `orchestration/test-runners.yaml` (+ `context/test-runners.override.yaml`
  del proyecto, si existe) y corre vía Execution Service — Carril B, sin
  confirmación humana (`orchestration/task-catalog.yaml`, type
  `test_execution`). Ver `agentes/qa-reviewer.md` sección 2 y
  `agentes/cybersecurity.md` sección 7 para cuándo aplica cada carril.

## Cuándo se activa

- Antes de pedirle al PM que corra un comando manual de exploración del
  proyecto (Architect/Tech-Lead).
- Antes de que QA-Reviewer/Cybersecurity armen una Action de test, para
  confirmar el formato esperado.
- Cuando el Orchestrator necesita recordar qué `type` del catálogo
  corresponde a una operación de proyecto.

## Qué NO hace esta skill

- No repite el diseño del Project Service ni del Execution Service — viven
  en `iron_ops/*.py`.
- No repite el catálogo de runners — vive en `orchestration/test-runners.yaml`.
- No decide si una operación necesita confirmación humana o no — esa regla
  vive exclusivamente en `orchestration/task-catalog.yaml` (campo
  `requires_human_confirmation`) y se aplica igual sin importar qué agente
  la consulte.
