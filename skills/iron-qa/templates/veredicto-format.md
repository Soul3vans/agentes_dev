# Plantilla de Veredicto de QA

Fuente canónica de este formato. Referenciado desde
`skills/iron-qa/SKILL.md`. No se duplica en ningún otro archivo — si otro
rol necesita citar el formato, referencia esta ruta.

    ## Veredicto de QA Review

    **Estado**: APROBADO | RECHAZADO | APROBADO CON OBSERVACIONES
    **Spec revisado**: specs/features/00X-nombre.md (versión: vX.X)

    ### 1. Comando de prueba propuesto (para confirmación en nion-cli)
    [comando exacto, o "No requiere ejecución" si la revisión es solo estática]

    ### 2. Checklist DoD
    - [x/ ] Código implementado según spec
    - [x/ ] Tests unitarios passing (X/Y tests, según salida real)
    - [x/ ] Adherencia a context/architecture.md
    - [x/ ] Chequeo básico de seguridad realizado
    - [x/ ] Cruce contra context/security-triggers.yaml realizado (comando ejecutado, ver sección 3)
    - [ ] [ítems específicos del spec]

    ### 3. Cruce con security-triggers.yaml
    **Comando ejecutado**: grep -riEf context/security-triggers.yaml <ruta>
    **Resultado**: [salida real, o "Sin coincidencias"]
    **Nota de escalación**: [si aplica: "⚠️ Requiere auditoría profunda de cybersecurity" + archivo/línea]

    ### 4. Hallazgos
    #### Bloqueantes (🔴)
    - Archivo / línea, problema, severidad.

    #### Menores (🟡)
    - Archivo / línea, problema.

    ### 5. Acción requerida
    [qué debe corregir el dev, si aplica, o "Ninguna" si aprobado sin observaciones]
