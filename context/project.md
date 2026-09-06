# context/project.md

## 1. Naturaleza del sistema

Este es un framework de agentes de IA reutilizable, agnóstico de stack tecnológico
y dominio de negocio. Está diseñado para operar sobre cualquier repositorio en dos
escenarios posibles:

- **Escenario A — Greenfield**: proyecto nuevo, sin código ni stack definido.
- **Escenario B — Brownfield**: proyecto existente, con stack, arquitectura y
  lógica de negocio ya establecidos.

La máxima autoridad de decisión es el **Project Manager humano** (el usuario).
Ningún agente decide de forma autónoma el rumbo del proyecto ni ejecuta acciones
irreversibles (commit, push, merge, deploy). Los agentes ejecutan, proponen y
reportan; el PM asigna, aprueba y autoriza.

## 2. Configuración de ejecución actual

- **Modelo de LLM**: un único modelo local de menor capacidad, asumiendo los 7
  roles definidos en `agentes/` (relación 1:7 — ver nota abajo sobre conteo de
  agentes).
- **Modo de operación**: LOCAL (sin tool-calling automático). Todo cambio de
  código se entrega en formato de diff (Formato de Propuesta de Cambio, definido
  en `orchestration/handoff-protocol.md`). El PM aplica los cambios manualmente.
- **Disciplina reforzada obligatoria** (compensa la menor capacidad del modelo):
  1. Cada invocación de rol carga únicamente su propio archivo `agentes/<rol>.md`
     más los archivos de `context/`/`specs/` estrictamente necesarios para la
     tarea. Nunca se carga "todo el proyecto" de una sola vez.
  2. Ejecución estrictamente secuencial entre roles. No se simula paralelismo.
  3. Al finalizar cada tarea, el agente debe repetir el checklist aplicable del
     `specs/` correspondiente, marcando ítem por ítem como cumplido, antes de
     entregar el resultado al PM.
  4. Ante cualquier ambigüedad no cubierta por `context/` o `specs/`, el agente
     debe detenerse y escalar al `orchestrator`/PM. Nunca improvisa criterio.
- **Ruta de escalado futura**: si se incorpora un segundo modelo de mayor
  capacidad, la migración recomendada es dividir la carga en:
  - Modelo A (alta capacidad): `architect`, `tech-lead`, `cybersecurity`
  - Modelo B (menor capacidad): `frontend-dev`, `backend-dev`, `qa-reviewer`
  Esta división vive documentada como tabla de configuración en
  `context/constraints.md` y no requiere rediseñar el sistema, solo reasignar
  qué modelo atiende qué archivo de `agentes/`.

## 3. Nota sobre el conteo de agentes

El sistema cuenta con 7 archivos de agente:

orchestrator.md → Meta-agente. Coordina el flujo: decide QUIÉN actúa y CUÁNDO.
No decide contenido técnico ni de negocio.

architect.md → Diseño técnico de alto nivel: patrones de diseño, comunicación 
entre servicios, esquema de base de datos, escalabilidad, mantenibilidad. 
Redacta ADRs.

tech-lead.md → Descomposición de tareas, cumplimiento de estándares de 
specs/constraints, gestión de dependencias, coordinación día a día entre 
frontend-dev y backend-dev.

frontend-dev.md → Implementación de interfaz, accesibilidad, i18n, rendimiento web.

backend-dev.md → Implementación de lógica de servidor, APIs, base de datos, 
performance de queries, logs.

qa-reviewer.md → Pruebas (unitarias, integración, E2E), revisión de PRs contra 
constraints.md, detección de deuda técnica.

cybersecurity.md → Auditoría de seguridad, OWASP Top 10, gestión de secretos, 
dependencias vulnerables.
