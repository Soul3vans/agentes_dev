# orchestration/workflow.md

## 1. Propósito

Este archivo define la máquina de estados y el ciclo de vida completo de una tarea 
dentro del sistema IRON. Es la fuente de verdad del “cómo” fluye el trabajo. 
El Orchestrator y todos los agentes deben respetarlo.

## 2. Estados del ciclo de vida

| Estado            | Descripción                                                                 | Quién puede cambiarlo          |
|-------------------|-----------------------------------------------------------------------------|--------------------------------|
| RECEIVED          | Solicitud recibida del PM                                                   | Orchestrator                   |
| CLASSIFIED        | Clasificada contra task-catalog.yaml                                        | Orchestrator                   |
| IN_PROGRESS       | Agente trabajando activamente                                               | Agente asignado                |
| WAITING_HUMAN     | Esperando confirmación o decisión del PM                                    | Cualquier agente / Orchestrator|
| VALIDATION        | En revisión de QA y/o Cybersecurity                                         | QA / Cybersecurity             |
| BLOCKED           | Hay hallazgos o decisiones pendientes de negociación con el PM              | Tech-Lead                      |
| DEFERRED          | Hallazgo o trabajo pospuesto y documentado en el estado central             | Tech-Lead                      |
| RESOLVED          | Trabajo completado y aceptado                                               | Tech-Lead                      |
| CLOSED            | Tarea cerrada, archivo de estado actualizado                                | Orchestrator / Tech-Lead       |

## 3. Reglas generales

- Ejecución estrictamente secuencial (1 modelo).
- Máximo 10 iteraciones de orquestación por tarea. Al superarlas → escalar al PM con diagnóstico.
- Ningún agente técnico puede empezar sin spec válido (salvo tipos con `entry_requirement: none`).
- El archivo central de estado del proyecto (`specs/01-planning.md` o `specs/00-status.md`) 
  debe consultarse al inicio de cada tarea y actualizarse al final de cada cambio significativo.
- Todo hallazgo de QA o Cybersecurity pasa obligatoriamente por Tech-Lead antes de cualquier otra acción.
- **Cybersecurity se activa siempre después de QA, en ambos escenarios,
  independientemente de si QA reportó hallazgos de seguridad.** El
  resultado de QA solo modula la prioridad/urgencia de la revisión de
  Cybersecurity, nunca su ocurrencia.

## 4. Flujos por tipo de tarea

### 4.1 Feature — Escenario A (Greenfield / módulo nuevo)

1. Orchestrator clasifica → Tech-Lead
2. Tech-Lead elabora / actualiza spec + contratos API si aplica
3. Si hay decisión arquitectónica → escala a Architect (ADR)
4. Tech-Lead asigna a Frontend-Dev y/o Backend-Dev
5. Devs implementan hasta declarar **módulo completamente finalizado**
6. Tech-Lead activa QA
7. QA ejecuta revisión + tests de integración
8. Tech-Lead activa Cybersecurity de forma obligatoria, haya o no hallazgos
   de QA (los hallazgos de QA solo afectan la prioridad/urgencia de la
   auditoría, nunca si esta ocurre)
9. Cybersecurity entrega reporte a Tech-Lead
10. Tech-Lead negocia con PM (resolver ahora vs diferir a spec)
11. Se actualiza el archivo central de estado
12. Cierre o nueva iteración según decisión del PM

### 4.2 Feature — Escenario B (Brownfield / proyecto avanzado)

1. Orchestrator clasifica → Tech-Lead
2. Tech-Lead solicita revisión inicial del estado actual
3. QA revisa el proyecto/módulo existente
4. Cybersecurity revisa después de QA
5. Ambos reportan hallazgos a Tech-Lead
6. Tech-Lead presenta al PM los hallazgos de seguridad y calidad
7. PM decide: resolver ahora / diferir documentado / aceptar riesgo
8. Solo después de esa decisión se planifica y desarrolla cualquier feature nueva
9. A partir de aquí se sigue el flujo de implementación normal (pasos 4-12 del Escenario A)

### 4.3 Bug trivial
Orchestrator → Dev de la capa afectada → notificación a Tech-Lead → registro en docs/bugs.md → cierre.

### 4.4 Bug complejo
Orchestrator → QA (diagnóstico) → Tech-Lead → (spec si hace falta) → Dev → QA → cierre.

### 4.5 Security audit explícita
Orchestrator → Cybersecurity → reporte a Tech-Lead → negociación con PM.

### 4.6 Ambiguous / Project question
Orchestrator responde o pregunta al PM. No delega a agentes técnicos hasta tener claridad.

## 5. Puntos de confirmación humana obligatorios

- Aprobación de plan de implementación de los Devs
- Aprobación de cada diff de código
- Ejecución de comandos de test o análisis (vía nion-cli)
- Decisión sobre hallazgos de QA/Cyber (inmediato vs diferido)
- Aceptación de ADRs blocking

## 6. Actualización del estado central

Tech-Lead actualiza el archivo de estado del proyecto al menos en estos momentos:
- Después de crear o versionar un spec
- Después de recibir reportes de QA o Cybersecurity
- Después de una decisión del PM sobre hallazgos
- Al declarar un módulo como completado
- Al cerrar una tarea
