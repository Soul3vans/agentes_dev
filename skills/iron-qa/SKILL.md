---
name: iron-qa
description: Activate when validating a completed module or reviewing a diff — running quality checks, cross-checking against security-triggers.yaml, integrating real execution evidence via nion-cli, and producing a structured verdict. Assumes agentes/qa-reviewer.md is already loaded for identity and rules.
---

# IRON QA — Skill de herramienta (nion-cli)

Esta skill **no redefine** identidad, alcance ni reglas del rol — eso vive
en `agentes/qa-reviewer.md` (fuente canónica, cargar siempre primero).
Esta skill agrega el **procedimiento operativo** para testear, cruzar
contra patrones de seguridad, y emitir veredictos a través de `nion-cli`.

## Cuándo se activa

- El módulo fue declarado completamente finalizado por Tech-Lead, con el
  criterio objetivo de `agentes/tech-lead.md`, sección 8.1 (DoD marcado
  ítem por ítem con evidencia) — Escenario A.
- O bien, se te asignó la revisión inicial de un proyecto existente —
  Escenario B.
- O bien, se te asignó un `code_review` puntual sobre un diff ya propuesto.

## Superpoder 1: proponer y ejecutar verificación real vía nion-cli

1. Proponés el comando exacto de prueba necesario (test unitario,
   integración, build) según el contrato de `context/tech-stack.md`,
   sección 1.1 ("QA-Reviewer / Cybersecurity").
2. Esperás confirmación del PM (`[Y/n]`) antes de asumir ejecución.
3. Si el PM aprueba: integrás la salida real (`stdout`/`stderr`) en tu
   veredicto. Nunca asumís un resultado de test sin esa salida (ver
   `context/constraints.md`, sección 10.2).
4. Si el PM rechaza: tu veredicto queda como "APROBADO CON OBSERVACIONES —
   pendiente de verificación en ejecución" (ver plantilla de veredicto).

## Superpoder 2: chequeo determinista de seguridad

Antes de cerrar cualquier veredicto, proponés vía `nion-cli` el comando:

    grep -riEf context/security-triggers.yaml <ruta_del_diff_o_módulo>

- Si hay coincidencias: las listás en la sección "Hallazgos" de tu
  veredicto y marcás la nota "⚠️ Requiere auditoría profunda de
  cybersecurity" si el patrón sugiere lógica de auth/crypto/sesión (ver
  `agentes/qa-reviewer.md`, sección 5).
- **Esto no reemplaza ni condiciona la activación de Cybersecurity.**
  Cybersecurity revisa siempre después de vos, haya o no coincidencias
  (ver `agentes/qa-reviewer.md`, sección 8, "Regla obligatoria"). El grep
  solo modula la prioridad/urgencia con la que `tech-lead` debe escalar.

## Formato de veredicto

El formato completo y obligatorio vive en
`skills/iron-qa/templates/veredicto-format.md` — usalo siempre, sin
improvisar una estructura distinta.

## Qué NO hace esta skill

- No corrige código (solo aprueba o rechaza) — regla dura del Principio 3.
- No decide si un hallazgo de seguridad es una vulnerabilidad confirmada
  (eso es Cybersecurity, exclusivamente).
- No envía hallazgos directo a devs o PM — siempre a través de Tech-Lead.
- No repite el protocolo de conteo de rechazos ni el flujo de diagnóstico
  de bugs complejos — están en `agentes/qa-reviewer.md`, secciones 4 y 6,
  y siguen aplicando íntegramente.
