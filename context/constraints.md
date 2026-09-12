---
version: 1.1.0
last_updated: 2026-09-02
updated_by: PM + Architect (auditoria IRON)
changelog:
  - 1.1.0: Añadido protocolo anti-alucinación (sección 10) y nota de memoria de agente (00-status.md)
  - 1.0.0: Versión inicial del framework, consolidada tras rondas de definición
---

# context/constraints.md

- Principios obligatorios del sistema: ver `context/principios.md` (fuente de verdad).

## 1. Snapshot de reglas de negocio del proyecto actual

> Esta sección se completa por `architect`/`tech-lead` al analizar cada
> proyecto concreto (Escenario A o B). En el framework base queda vacía.

- Dominio de negocio: _(pendiente de completar por proyecto)_
- Reglas de negocio críticas no negociables: _(pendiente)_
- Restricciones regulatorias/legales aplicables (si las hay): _(pendiente)_
- Licencia del proyecto: _(pendiente — ver sección 7 para default)_

## 2. Umbrales de calidad (reglas duras, aplican siempre)

- Cobertura de tests: **> 80%** general, **> 90%** en lógica de negocio crítica.
- Bug Escape Rate: **< 5%**.
- First-Pass Yield (PRs aprobados sin corrección mayor): **> 85%**.
- Complejidad ciclomática por función:
  - **≤ 10** → aceptable.
  - **11–15** → warning, `qa-reviewer` solicita justificación.
  - **> 15** → rechazo automático, salvo excepción documentada vía ADR
    (`architect`) que justifique la complejidad inherente del caso.
- Deuda técnica marcada (TODO/FIXME): límite de referencia **≤ 20** por
  proyecto activo. La herramienta de medición (grep manual, SonarQube, jscpd,
  u otra) queda a criterio de `tech-lead` según el stack detectado en
  `context/tech-stack.md`. Igual criterio aplica para detección de funciones
  duplicadas (límite de referencia **≤ 3** instancias antes de refactor
  obligatorio).

## 3. Definition of Done (DoD)

Checklist base aplicable a toda tarea, con variantes según tipo:

**Feature nueva:**
- [ ] Código implementado según spec (`specs/`)
- [ ] Tests unitarios + integración escritos y en verde
- [ ] Sin violaciones de este archivo (`constraints.md`)
- [ ] Revisado y aprobado por `qa-reviewer`
- [ ] Documentación técnica actualizada (endpoints, componentes, etc.)
- [ ] Sin vulnerabilidades críticas/altas (validado por `cybersecurity`)
- [ ] ADR redactado si hubo decisión arquitectónica relevante

**Bugfix:**
- [ ] Causa raíz identificada y documentada
- [ ] Test de regresión añadido que reproduce el bug original
- [ ] Fix validado contra ese test
- [ ] Revisado por `qa-reviewer`

**Refactor:**
- [ ] Comportamiento externo sin cambios (tests existentes siguen en verde)
- [ ] Mejora de complejidad/legibilidad medible o justificada
- [ ] Sin nueva funcionalidad mezclada en el mismo cambio

**Hotfix:**
- [ ] Fix mínimo y acotado al problema urgente
- [ ] Test de regresión añadido (puede ser posterior al deploy si la urgencia
      lo justifica, pero es obligatorio antes de cerrar la tarea)
- [ ] Notificación explícita al PM del riesgo asumido

## 4. Convenciones (enfoque híbrido)

- **Universal (todo proyecto, todo stack):**
  - Commits: Conventional Commits, en inglés (`feat:`, `fix:`, `refactor:`,
    `docs:`, `test:`, `chore:`).
  - Ramas: `feature/<nombre>`, `fix/<nombre>`, `hotfix/<nombre>`,
    `refactor/<nombre>`.
- **Específico por proyecto (decide `tech-lead` según stack detectado en
  `context/tech-stack.md`):**
  - Nomenclatura de variables/funciones (`camelCase`, `snake_case`, etc.)
  - Estructura de carpetas interna
  - Convención de nombres de archivos de test

## 5. Seguridad (resumen — detalle completo en `agentes/cybersecurity.md`)

Reglas no negociables, sin excepción salvo aprobación explícita del PM:
- Nunca secretos (API keys, contraseñas, tokens) en código versionado.
- Siempre validar y sanitizar inputs de usuario antes de procesarlos.
- Siempre HTTPS/TLS en cualquier comunicación fuera de entornos de desarrollo
  local aislado.
- Ver `agentes/cybersecurity.md` para el detalle técnico completo (OWASP Top
  10, gestión de dependencias vulnerables, auditorías SAST/DAST).
- Chequeo automatizable de patrones sensibles: ver `context/security-triggers.yaml`
  (lista determinista, consumida vía `grep` por `qa-reviewer` a través de
  `nion-cli`). Su aparición en un diff no es prueba de vulnerabilidad, pero
  obliga a documentar el hallazgo y darle prioridad en la revisión de
  `cybersecurity`.

## 6. Manejo de errores, logging y observabilidad

- Referencia obligatoria: `context/architecture.md`, sección 5 (estándar
  global de manejo de errores). No se duplica aquí para evitar
  desincronización; `qa-reviewer` audita contra esa sección.
- Logging estructurado obligatorio en todo error capturado (contexto, módulo,
  timestamp, identificador de traza si aplica).

## 7. Licencias

- Por defecto, se **prohíbe el uso de librerías con licencia GPL** (o
  copyleft fuerte equivalente) en proyectos privados/propietarios, salvo
  aprobación explícita del PM.
- **Excepción activa**: si el PM declara el proyecto como software libre desde
  su concepción, esta restricción se levanta y debe documentarse en la
  sección 1 de este archivo (Snapshot del proyecto), especificando la licencia
  elegida (GPL, MIT, Apache 2.0, etc.).

## 8. Gestión de dependencias (complementa `context/tech-stack.md`)

- Modelo reactivo por defecto: `tech-lead` audita/actualiza dependencias solo
  cuando el PM lo solicita explícitamente.
- **Única excepción**: si se detecta una vulnerabilidad de **severidad
  CRÍTICA** en una dependencia durante cualquier tarea (aunque no sea el
  objetivo de esa tarea), el agente que la detecte debe **alertar
  inmediatamente al PM**, sin ejecutar ninguna actualización por su cuenta.
  La decisión de actuar de inmediato o esperar sigue siendo del PM.

## 9. Límites operativos del propio framework de agentes

- **Concurrencia de agentes**: 1 (ejecución estrictamente secuencial). Este
  valor solo se revisa si se migra a la arquitectura de 2+ modelos descrita
  en `context/project.md`, sección 2.
- **Ventana de contexto por invocación**: ~32K tokens (referencia para la
  familia Qwen2.5-Coder). Cada invocación de rol debe cargar solo lo
  estrictamente necesario (su `agentes/<rol>.md` + archivos puntuales de
  `context/`/`specs/`), nunca el proyecto completo.
- **Máximo de iteraciones de orquestación por tarea**: 10 (anti-bucle). Si se
  supera, el `orchestrator` detiene el ciclo y escala al PM con diagnóstico.
- **Escalamiento por rechazos repetidos**: tras 3 rechazos consecutivos de
  `qa-reviewer` sobre la misma propuesta, el caso escala automáticamente a
  `tech-lead` para revisión de criterio (evita bucles de corrección infinita
  por criterios subjetivos no definidos aquí).
- **Prohibición de alcance**: ningún agente puede modificar archivos fuera del
  alcance explícito de la tarea asignada. Cualquier cambio fuera de alcance
  detectado como necesario debe reportarse como hallazgo, no ejecutarse
  directamente.
  **Archivo de memoria del agente**: `specs/00-status.md` es el resumen vivo
  del proyecto. Orchestrator debe consultarlo en cada nueva solicitud;
  Tech-Lead es el único autorizado a actualizarlo.

  **Límite numérico obligatorio** (calibrado para qwen2.5-coder:1.5b/3b,
  context length 32.768 tokens, operado con margen de seguridad en
  30.000-31.000): el archivo no debe superar **800 tokens aproximados**,
  equivalentes de referencia a **~100 líneas** o **~600 palabras** de
  markdown. Este archivo se carga en *cada* invocación del Orchestrator
  (ver `agentes/orchestrator.md`, sección 8), por lo que debe representar
  una fracción mínima del presupuesto total de contexto, dejando espacio
  para el archivo de rol, el spec activo, el handoff recibido y la
  conversación en curso.

  Verificación práctica (sin necesidad de tokenizer): Tech-Lead ejecuta
  `wc -l specs/00-status.md` y `wc -w specs/00-status.md` antes de cerrar
  cualquier actualización. Si supera ~100 líneas o ~600 palabras, debe
  mover el detalle excedente a `docs/debt.md` o `docs/bugs.md` (fuentes de
  verdad) y dejar solo el resumen y la referencia en `00-status.md`.

  Los detalles de deuda y bugs viven en `docs/debt.md` y `docs/bugs.md`
  (fuentes de verdad) — nunca se duplican en `00-status.md`.
  
## 10. Protocolo anti-alucinación y verificación de existencia (obligatorio)

Todo agente debe cumplir estas reglas operativas. No basta con "no inventar".

### 10.1 Verificación obligatoria de existencia
Antes de afirmar que existe un archivo, directorio, función, clase, endpoint,
dependencia o comportamiento del código, el agente **debe** proponer un comando
de verificación (ej. `ls`, `find`, `grep`, `cat package.json`, etc.) que se 
ejecute via nion-cli. Solo después de recibir la salida real puede tratarlo 
como KNOWN.

### 10.2 Estados de conocimiento obligatorios (fuente canónica)

Esta sección es la **única fuente de verdad** de las definiciones de estado
de conocimiento en todo IRON. Ningún otro archivo (`agentes/*.md`,
`orchestration/*.md`) debe repetir estas definiciones completas — deben
referenciar esta sección por número (`context/constraints.md`, sección
10.2) y, si necesitan una variante específica de su dominio (ej. la
clasificación de hallazgos de seguridad en `agentes/cybersecurity.md`,
sección 4), declararla explícitamente como una **extensión**, no como una
redefinición paralela.

Toda afirmación relevante debe etiquetarse explícitamente:
- **KNOWN**: confirmado con evidencia real.
- **INFERRED**: conclusión derivada de información disponible.
- **UNKNOWN**: información que no se tiene.
- **REQUIRES_VERIFICATION**: debe comprobarse antes de actuar o afirmar.

Nunca se presenta un UNKNOWN o REQUIRES_VERIFICATION como hecho.

### 10.3 Prohibiciones absolutas
- Inventar archivos, rutas, funciones, firmas, librerias, endpoints.
- Asumir que un endpoint definido en un contrato ya está implementado.
- Asumir requisitos que no estén escritos en el spec o en el archivo de estado.
- Afirmar el resultado de test o análisis sin la salida real de nion-cli.

### 10.4 Evidencia de afirmaciones críticas
Cualquier afirmación sobre estado del código, existencia de archivos, 
resultados de tests o hallasgos de seguridad debe ir acompañada de evidencia 
o marcarse como REQUIRES_VERIFICATION.

### 10.5 Validación en handoffs
El agente que recibe un handoffs debe tratar como REQUIRES_VERIFICATION 
cualquier afirmación del agente anterior que no traiga evidencia real.

### 10.6 Regla especial para Developers
Antes de proponer un diff que modifica un archivo existente, el Developer 
debe verificar que el archivo existe y mostrar el fragmento relevante 
(o el resultado del comando de verificación).
