---
name: iron-handoff
description: Generate or validate IRON handoffs between agents. Use when transferring work, reporting status between roles, or ensuring context is not lost. Enforces the official handoff format.
---

# IRON Handoff

Produce or validate handoffs using the mandatory format from handoff-protocol.md.

## Hard rules

- Never invent decisions, evidence or files.
- Always include Knowledge states (KNOWN / INFERRED / UNKNOWN / REQUIRES_VERIFICATION).
- Findings from QA or Cyber must be routed only to Tech-Lead.
- Keep the handoff concise and limited to the minimum context needed by the receiver.

## Mandatory format

## HANDOFF

**De**: [AGENTE_ORIGEN]
**Para**: [AGENTE_DESTINO]
**Tarea / Spec**: ...
**Estado actual**: ...
**Escenario**: A / B / N/A

### 1. Contexto mínimo cargado
### 2. Decisiones ya tomadas
### 3. Evidencias
### 4. Incertidumbres
### 5. Hallazgos abiertos (si existen)
### 6. Próxima acción esperada
### 7. Bloqueadores actuales
