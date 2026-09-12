# context/tech-stack.md

## 1. Stack tecnológico del propio sistema de agentes

Este framework de agentes se ejecuta en el siguiente entorno:

- **Entornos soportados**: Termux (Android/Linux) y VSCode (extensión).
- **Modelo de LLM actual**: Qwen (modelo local), operando en configuración 1:7
  (un único modelo asumiendo los 7 roles definidos en `agentes/`), bajo el modo
  de operación LOCAL descrito en `context/project.md` (sección 8).
- **Modo de propuesta de cambios**: diffs unificados, sin ejecución automática
  de comandos, commits ni tests sin aprobación explícita del PM.
- Esta sección debe actualizarse si se cambia de entorno de ejecución, se migra
  a una API con tool-use (modo AGÉNTICO), o se incorpora un segundo modelo
  (ver ruta de escalado en `context/project.md`, sección 2).

## 1.1 Contrato mínimo de `nion-cli` (estado actual, runtime real)

Esta sección define el alcance funcional **verificado y exigible hoy** de
`nion-cli`. Cualquier capacidad no descrita aquí (API REST, webhooks,
aplicación automática sin confirmación, ejecución concurrente) pertenece a
`orchestration/nion-cli-api.md`, `orchestration/concurrency.md` y
`orchestration/task-queue.md` — marcados **DISEÑO FUTURO** — y ningún agente
debe asumir que están disponibles.

### Operaciones soportadas por rol

**Frontend-Dev / Backend-Dev**
1. Proponen un cambio como diff unificado (o bloque de código con ruta
   explícita para archivos nuevos).
2. `nion-cli` muestra el diff al PM y solicita confirmación (`[Y/n]`).
3. Si el PM aprueba: `nion-cli` aplica el diff y, si corresponde, ejecuta el
   comando asociado (build/test/dev server), devolviendo `stdout`/`stderr`
   real al agente.
4. Si el PM rechaza: no se aplica nada. El agente no continúa hasta recibir
   indicación del PM o de `tech-lead`.

**QA-Reviewer / Cybersecurity**
1. Proponen el comando exacto de verificación/análisis necesario (tests,
   linter, `grep` contra `context/security-triggers.yaml`, `npm audit`,
   etc.).
2. `nion-cli` muestra el comando al PM y solicita confirmación (`[Y/n]`).
3. Si el PM aprueba: `nion-cli` lo ejecuta y devuelve `stdout`/`stderr` real.
4. Si el PM rechaza: el veredicto queda como "APROBADO CON OBSERVACIONES —
   pendiente de verificación en ejecución" (QA) o el hallazgo se marca como
   "No verificado — pendiente de aprobación de ejecución" (Cyber), nunca
   como hecho confirmado.

### Regla de estado de conocimiento

Ningún agente puede tratar como **KNOWN** un resultado de ejecución
(aplicación de diff, resultado de test, salida de análisis) sin haber
recibido la salida real de `nion-cli` en ese mismo turno o en un handoff que
la incluya explícitamente (ver `orchestration/handoff-protocol.md`, sección
3).

### Estado de implementación

- Confirmación `[Y/n]` antes de aplicar/ejecutar: **REQUIRES_VERIFICATION**
  — descrita en todos los `agentes/*.md`, pero no hay evidencia en este
  repositorio de que `nion-cli` la implemente; el único artefacto real
  disponible es el wrapper `scripts/iron` (invocación de rol + prompt).
- Aplicación de diffs y captura de `stdout`/`stderr`: **REQUIRES_VERIFICATION**
  por el mismo motivo.
- Hasta que estas dos capacidades se confirmen con evidencia (ej. código
  fuente de `nion-cli` revisado, o una ejecución real documentada), todo
  agente debe tratar "el PM confirmó y `nion-cli` ejecutó" como una
  afirmación que requiere verificación explícita en cada handoff, no como
  un hecho asumido por defecto.

## 2. Señales de detección de stack (Escenario B — Brownfield)

Al analizar un repositorio existente, el `orchestrator` debe buscar, en orden
de prioridad, los siguientes archivos característicos por ecosistema:

### Node.js / JavaScript / TypeScript
- `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- `tsconfig.json` (indica TypeScript)
- `next.config.js`, `vite.config.ts`, `nuxt.config.ts`, `angular.json` (framework)

### Python
- `requirements.txt`, `Pipfile`, `pyproject.toml`, `poetry.lock`
- `manage.py` (indica Django), `app.py`/`main.py` con imports de Flask/FastAPI

### PHP
- `composer.json`, `composer.lock`
- `artisan` (indica Laravel)

### Java / Kotlin
- `pom.xml` (Maven), `build.gradle`/`build.gradle.kts` (Gradle)
- `application.properties`/`application.yml` (indica Spring Boot)

### Go
- `go.mod`, `go.sum`

### Ruby
- `Gemfile`, `Gemfile.lock`
- `config/routes.rb` (indica Rails)

### .NET / C#
- `*.csproj`, `*.sln`, `appsettings.json`

### Rust
- `Cargo.toml`, `Cargo.lock`

### Señales transversales (cualquier stack)
- `Dockerfile`, `docker-compose.yml` (containerización)
- `.github/workflows/`, `.gitlab-ci.yml` (CI/CD existente)
- `.env`, `.env.example` (variables de entorno)
- Carpeta `tests/`, `__tests__/`, `spec/` (convención de testing ya adoptada)

El `orchestrator` reporta al PM el stack detectado y su nivel de confianza
(alta/media/baja) antes de que `architect`/`tech-lead` inicien cualquier
planificación. Ante señales contradictorias (ej. mezcla de ecosistemas sin
justificación de microservicios), se reporta como hallazgo y se pregunta al PM.

## 3. Política de stack para Escenario A (Greenfield)

- **No existe stack por defecto predefinido.** El `architect` debe preguntar
  siempre al PM el tipo de proyecto, restricciones y preferencias antes de
  proponer cualquier tecnología (ver batería de preguntas en `specs/00-intake.md`).
- Una vez el PM define o aprueba el stack, **siempre se usa la última versión
  LTS o estable disponible** del lenguaje/framework/librería principal, salvo
  que el PM indique explícitamente una versión distinta por razón de
  compatibilidad u otro motivo justificado.
- El `architect` debe verificar la fecha de fin de soporte (EOL) de cualquier
  versión antes de proponerla. Nunca se recomienda una versión próxima a EOL
  (umbral: menos de 6 meses de soporte restante) sin advertirlo explícitamente.

## 4. Política de versiones (ambos escenarios)

- Nunca usar versiones **EOL (end-of-life)** de lenguajes, frameworks o
  librerías sin que el PM lo apruebe explícitamente y por escrito (queda
  registrado como decisión en un ADR vía `architect`).
- Nunca usar versiones con **CVEs críticos o altos sin parche disponible**.
- En Escenario B, si el stack detectado ya usa versiones EOL o vulnerables,
  esto se reporta como deuda técnica (ver `specs/01-planning.md`) pero **no**
  se actualiza de forma proactiva (ver sección 6).

## 5. Librerías, patrones y prácticas prohibidas globalmente

Prohibiciones válidas para cualquier stack, sin excepción, salvo autorización
explícita y documentada del PM. Esta lista se reitera y profundiza en
`context/constraints.md` y `agentes/cybersecurity.md`:

- Uso de `eval()` o equivalentes de ejecución dinámica de código no confiable.
- Almacenamiento de contraseñas, tokens o secretos en texto plano (en código,
  `.env` versionado, logs, o base de datos sin hashing/cifrado).
- ORMs o query builders para consultas complejas de alto rendimiento donde el
  SQL nativo optimizado sea claramente superior (decisión caso a caso,
  documentada por `architect` en ADR).
- Librerías deprecadas o sin mantenimiento activo (> 2 años sin releases) para
  funciones críticas de seguridad (auth, criptografía, sanitización de inputs).
- Librerías con vulnerabilidades históricas conocidas y no resueltas (ejemplo
  de referencia: `request` en Node.js — deprecada; versiones de `lodash`
  anteriores a parches de seguridad conocidos).
- Concatenación directa de inputs de usuario en queries SQL (sin prepared
  statements/parametrización) — riesgo de SQL Injection.
- Deshabilitar validaciones de certificados TLS/SSL en cualquier entorno que
  no sea testing local aislado.

## 6. Gestión de actualización de dependencias

- El sistema opera en modo **reactivo**: `tech-lead` audita y actualiza
  dependencias únicamente cuando el PM lo solicita explícitamente.
- No se ejecutan actualizaciones automáticas ni programadas por ciclo/sprint.
- Cuando el PM solicita una auditoría, `tech-lead` debe:
  1. Listar dependencias desactualizadas y vulnerabilidades detectadas
     (vía `npm audit`, `pip-audit`, `composer audit`, o equivalente).
  2. Evaluar breaking changes de las versiones nuevas contra `specs/` vigentes.
  3. Proponer un plan de actualización priorizado por severidad de riesgo,
     sin ejecutar cambios hasta aprobación del PM.
