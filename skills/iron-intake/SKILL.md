---
name: iron-intake
description: Convert free-text PM requests, user stories or use cases into a structured IRON spec using the mandatory template. Use at the start of any new feature before implementation.
---

# IRON Intake

Transform raw PM input into a complete, actionable spec. You act under Tech-Lead authority.

## Hard rules

- Never invent requirements that the PM did not state or clearly imply.
- Mark every unclear point as REQUIRES_VERIFICATION or ask the PM.
- Do not start implementation. Only produce the spec.
- Follow the mandatory template exactly. Do not omit sections.
- Load only the minimum context (this skill + current 00-status if needed).

## Mandatory spec template

# Spec: <nombre feature>

## Objetivo de negocio
[1-2 párrafos]

## Criterios de aceptación (checklist verificable)
- [ ] ...

## Alcance
### Incluye
- ...
### NO incluye (explícitamente)
- ...

## Dependencias
- **Specs previos**: ...
- **ADRs**: ...
- **Técnicas**: ...

## Asignación
- **frontend-dev**: ...
- **backend-dev**: ...
- **Contrato API**: ver sección Contratos si aplica

## Riesgo
- **Nivel**: low / medium / high
- **Razón**: ...

## Contratos (si la feature toca frontend y backend)
### API endpoints
MÉTODO /ruta
Body: { ... }
Response: 200 { ... } | 4XX { error: ... }

## Definición de "Hecho" (DoD)
- [ ] Código implementado
- [ ] Tests unitarios passing
- [ ] Tests de integración passing (si aplica)
- [ ] Code review aprobado por qa-reviewer
- [ ] Documentación actualizada (si aplica)
- [ ] Sin vulnerabilidades críticas/altas (cybersecurity)

## Cambios
- v1.0 (fecha): versión inicial

## Procedure

1. Read the PM free text / user story / use case.
2. Extract only what is explicit or strongly implied.
3. Fill every section of the template.
4. List open questions under a final "## Preguntas al PM" section if anything is unclear.
5. Hand the completed spec to Tech-Lead for confirmation before any development starts.
