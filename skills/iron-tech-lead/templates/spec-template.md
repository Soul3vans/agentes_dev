# Plantilla de Spec — IRON

Fuente canónica de este formato. Antes vivía duplicado en
`agentes/tech-lead.md` sección 3 y en `scripts/roles/iron-intake.md`
(carpeta eliminada). Referenciado desde `skills/iron-tech-lead/SKILL.md`.
No se duplica en ningún otro archivo — cualquier rol futuro (ej. una skill
de intake que se recree) debe referenciar esta ruta, nunca copiar el
contenido.

    # Spec: <nombre feature>

    ## Objetivo de negocio
    [1-2 párrafos: qué problema resuelve, por qué es importante]

    ## Criterios de aceptación (checklist verificable)
    - [ ] Criterio 1
    - [ ] Criterio 2

    ## Alcance
    ### Incluye
    - ...
    ### NO incluye (explícitamente)
    - ...

    ## Dependencias
    - **Specs previos**: `specs/features/<archivo>.md`
    - **ADRs**: `docs/adr/<archivo>.md`
    - **Técnicas**: ej. "Requiere que el endpoint `/api/users` ya exista"

    ## Asignación
    - **frontend-dev**: tareas N, N+1...
    - **backend-dev**: tareas N, N+1...
    - **Contrato API**: ver sección "Contratos" si aplica

    ## Riesgo
    - **Nivel**: low / medium / high
    - **Razón**: breve justificación

    ## Contratos (si la feature toca frontend y backend)
    ### API endpoints
    MÉTODO /ruta
    Body: { ... }
    Response: 200 { ... } | 4XX { error: string }

    ## Definición de "Hecho" (DoD)
    - [ ] Código implementado
    - [ ] Tests unitarios passing
    - [ ] Tests de integración passing (si aplica)
    - [ ] Code review aprobado por `qa-reviewer`
    - [ ] Documentación actualizada (si aplica)
    - [ ] Sin vulnerabilidades críticas/altas (`cybersecurity`)

    ## Cambios
    - v1.0 (fecha): versión inicial

    ## Preguntas al PM (si aplica)
    - [listar solo si algo quedó ambiguo o sin confirmar]
