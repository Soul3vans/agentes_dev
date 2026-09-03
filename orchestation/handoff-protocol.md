# orchestation/handoff-protocol.md

## 1. Propósito

Define el formato obligatorio de traspaso de información entre agentes. 
Garantiza que no se pierda contexto, decisiones ni evidencias, y reduce alucinaciones 
de “qué se acordó antes”.

## 2. Regla general

Todo traspaso entre agentes debe usar el formato estructurado de abajo. 
No se permiten traspasos informales ni resúmenes ambiguos.

## 3. Formato de Handoff (obligatorio)

```markdown
## HANDOFF

**De**: [AGENTE_ORIGEN]
**Para**: [AGENTE_DESTINO]
**Tarea / Spec**: [identificador o nombre]
**Estado actual**: [uno de los estados definidos en workflow.md]
**Escenario**: A (Greenfield) / B (Brownfield) / N/A

### 1. Contexto mínimo cargado
- Lista exacta de archivos que el agente destino debe considerar

### 2. Decisiones ya tomadas
- Lista de decisiones firmes (con fecha o versión si aplica)

### 3. Evidencias
- Resultados reales de comandos, tests o análisis (stdout/stderr cuando existan)

### 4. Incertidumbres
- KNOWN: ...
- INFERRED: ...
- UNKNOWN: ...
- REQUIRES_VERIFICATION: ...

### 5. Hallazgos abiertos (si existen)
- Resumen de hallazgos de QA/Cyber pendientes de decisión del PM
- Enlace o referencia al archivo central de estado

### 6. Próxima acción esperada
- Qué debe hacer exactamente el agente destino

### 7. Bloqueadores actuales
- Lista de lo que impide avanzar (si los hay)
```

## 4. Reglas específicas por tipo de traspaso

- **Orchestrator → cualquier agente**: incluir siempre el type de tarea y los requires_context del catálogo.
- **Tech-Lead → Dev**: incluir siempre el spec completo + contrato API si existe + declaración de si el módulo se considera finalizado o no.
- **Dev → Tech-Lead / QA**: incluir siempre el plan ejecutado, los diffs aplicados y el estado de los tests.
- **QA → Cybersecurity**: incluir el reporte de QA completo y la razón por la que se activa Cyber.
- **QA / Cybersecurity → Tech-Lead**: usar el formato de reporte definido en sus respectivos archivos de agente + este handoff.
- **Cualquier agente → Orchestrator**: incluir diagnóstico claro cuando se escala por bucle, ambigüedad o bloqueo.

## 5. Prohibiciones

- No omitir la sección de Incertidumbres.
- No presentar UNKNOWN o REQUIRES_VERIFICATION como hechos.
- No traspasar hallazgos de seguridad o calidad directamente a los Devs o al PM (siempre pasan por Tech-Lead).
- No inventar archivos, decisiones o evidencias que no existan.

## 6. Actualización del estado central

Después de todo handoff significativo, Tech-Lead es responsable de reflejar el cambio 
en el archivo central de estado del proyecto.
