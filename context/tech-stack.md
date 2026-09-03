# context/tech-stack.md

## 1. Stack tecnológico del propio sistema de agentes

Este framework de agentes se ejecuta en el siguiente entorno:

- **Entornos soportados**: Termux (Android/Linux) y VSCode (extensión).
- **Modelo de LLM actual**: Qwen (modelo local), operando en configuración 1:7
  (un único modelo asumiendo los 7 roles definidos en `agents/`), bajo el modo
  de operación LOCAL descrito en `context/project.md` (sección 8).
- **Modo de propuesta de cambios**: diffs unificados, sin ejecución automática
  de comandos, commits ni tests sin aprobación explícita del PM.
- Esta sección debe actualizarse si se cambia de entorno de ejecución, se migra
  a una API con tool-use (modo AGÉNTICO), o se incorpora un segundo modelo
  (ver ruta de escalado en `context/project.md`, sección 2).

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
`context/constraints.md` y `agents/cybersecurity.md`:

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
