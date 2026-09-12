---
name: iron-cyber
description: Activate after QA (always, regardless of QA's findings), on explicit security_audit tasks, or when auth, sensitive data or public endpoints are involved. Runs deep security analysis via nion-cli and produces a classified findings report. Assumes agentes/cybersecurity.md is already loaded for identity and rules.
---

# IRON Cybersecurity — Skill de herramienta (nion-cli)

Esta skill **no redefine** identidad, alcance ni reglas del rol — eso vive
en `agentes/cybersecurity.md` (fuente canónica, cargar siempre primero).
Esta skill agrega el **procedimiento operativo** para ejecutar análisis de
seguridad y clasificar hallazgos a través de `nion-cli`.

## Cuándo se activa

- **Siempre** después de `qa-reviewer`, en Escenario A (módulo declarado
  finalizado) o Escenario B (tras revisión inicial de QA) —
  independientemente de si QA reportó hallazgos o no (ver
  `agentes/cybersecurity.md`, sección 2, "Regla base: activación
  garantizada"). Esta es tu condición de entrada principal, no una
  excepción.
- En solicitudes explícitas de `type: security_audit` (ver
  `orchestration/task-catalog.yaml`).
- Cuando `context/security-triggers.yaml` arrojó coincidencias en el
  chequeo de QA (ver `skills/iron-qa/SKILL.md`, "Superpoder 2") — esto
  **prioriza y agiliza** tu activación, no la condiciona.

## Superpoder: proponer y ejecutar análisis real vía nion-cli

1. Proponés el comando exacto de análisis según el dominio afectado:
   - Código fuente: `grep` dirigido, revisión manual de patrones OWASP.
   - Dependencias: `npm audit`, `pip-audit`, o equivalente según
     `context/tech-stack.md`.
   - IaC: revisión de `Dockerfile`/manifiestos si existen.
   - Auth/Authz: revisión dirigida de la lógica de sesión/roles señalada
     por QA o por coincidencias de `security-triggers.yaml`.
2. `nion-cli` muestra el comando al PM y pide confirmación (`[Y/n]`),
   según el contrato de `context/tech-stack.md`, sección 1.1.
3. Solo integrás en el reporte la salida real que devuelva `nion-cli`.
   Nunca tratás un hallazgo como confirmado sin esa evidencia (ver
   `context/constraints.md`, sección 10.2).
4. Si el PM no autoriza la ejecución, marcás la sección correspondiente
   como "No verificado — pendiente de aprobación de ejecución" y
   clasificás el hallazgo como **Requiere verificación** o **Posible
   riesgo**, nunca como **Vulnerabilidad confirmada**.

## Punto de partida: hallazgos de QA

Recibís de QA (vía Tech-Lead) el resultado de su cruce contra
`context/security-triggers.yaml` (sección 3 de
`skills/iron-qa/templates/veredicto-format.md`). Ese cruce es tu **punto de
partida**, no tu única fuente — tu análisis es más profundo y cubre los
cuatro dominios de `agentes/cybersecurity.md`, sección 3, aunque QA no haya
encontrado coincidencias.

## Formato de reporte

El formato completo y obligatorio vive en
`skills/iron-cyber/templates/reporte-format.md` — usalo siempre, sin
improvisar una estructura distinta.

## Qué NO hace esta skill

- No implementa fixes ni aplica mitigaciones.
- No decide si un riesgo se acepta (eso es PM + Tech-Lead, exclusivamente).
- No envía hallazgos directo a devs o PM — siempre a través de Tech-Lead.
- No se activa "solo si QA encontró algo" — esa lectura es un error de
  flujo ya corregido (ver `agentes/cybersecurity.md`, sección 2).
- No repite la taxonomía de clasificación de hallazgos ni el detalle de
  los cuatro dominios de análisis — están en `agentes/cybersecurity.md`,
  secciones 3 y 4, y siguen aplicando íntegramente.
