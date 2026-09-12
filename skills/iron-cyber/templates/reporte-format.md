# Plantilla de Reporte de Cybersecurity

Fuente canónica de este formato (idéntica en estructura a la ya definida
en `agentes/cybersecurity.md`, sección 6 — se traslada aquí para que la
skill sea autocontenida en su procedimiento operativo). No se duplica en
ningún otro archivo.

    ## Reporte de Cybersecurity

    **Escenario**: A (Greenfield) / B (Brownfield)
    **Módulo / Feature revisado**: ...
    **Fecha**: ...
    **Activado por**: post-QA (activación garantizada) / trigger de security-triggers.yaml / solicitud explícita de security_audit

    ### 1. Resumen ejecutivo
    - Cantidad de hallazgos por severidad y por clasificación.

    ### 2. Punto de partida (cruce de QA)
    - Resultado del grep de QA contra security-triggers.yaml (sección 3 del veredicto de QA)
    - Coincidencias: [listado, o "Sin coincidencias — igual se realiza auditoría completa"]

    ### 3. Hallazgos
    #### Vulnerabilidades confirmadas (bloqueantes)
    - Archivo / línea / componente
    - Descripción
    - Evidencia (comando ejecutado + salida real si el PM autorizó)
    - Impacto potencial
    - Recomendación de mitigación (sin implementar)

    #### Posibles riesgos
    - ...

    #### Requiere verificación
    - ...

    ### 4. Dependencias y SCA
    - ...

    ### 5. IaC y configuración
    - ...

    ### 6. Auth / Authz / Lógica de negocio
    - ...

    ### 7. Comandos de verificación propuestos
    - Lista de comandos exactos que deberían ejecutarse vía nion-cli para confirmar hallazgos.

    ### 8. Recomendación a tech-lead
    - Qué debe negociarse con el PM de inmediato.
    - Qué puede diferirse a un spec.
