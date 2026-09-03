# context/architecture.md

## 1. Principios de diseño arquitectónico (obligatorios)

Estos principios aplican a nivel de código y estructura técnica, en cualquier
stack o proyecto que pase por este sistema:

1. **SOLID**: Single Responsibility, Open/Closed, Liskov Substitution,
   Interface Segregation, Dependency Inversion. Aplican especialmente en
   backend-dev y frontend-dev al diseñar clases/módulos/componentes.
2. **Separación de capas**: presentación (UI/controllers) → lógica de negocio
   (services/use cases) → acceso a datos (repositories/DAO). Ninguna capa
   accede directamente a una capa no adyacente (ej. un controller nunca
   consulta la base de datos directamente).
3. **Inyección de dependencias**: los módulos reciben sus dependencias
   (servicios, repositorios, clientes externos) en vez de instanciarlas
   internamente. Facilita testing y desacoplamiento.
4. **Responsabilidad única a nivel de módulo/servicio**: cada módulo, clase o
   servicio resuelve un único propósito claramente delimitado. Si un módulo
   requiere "y" en su descripción para explicarse, probablemente debe dividirse.
5. **DRY con límite razonable**: evitar duplicación de lógica de negocio, pero
   sin caer en sobre-abstracción prematura. Regla práctica: duplicar hasta la
   tercera repetición antes de abstraer (evita abstracciones equivocadas).
6. **Diseño basado en contratos**: interfaces, tipos y contratos de API
   (OpenAPI/GraphQL schema) se definen **antes** de implementar. El
   `architect` y `backend-dev`/`frontend-dev` deben acordar el contrato antes
   de escribir lógica interna.
7. **Minimización de complejidad estructural**: funciones pequeñas (idealmente
   < 40 líneas), archivos modulares con un único propósito, evitar anidamiento
   excesivo (máximo 3 niveles de indentación como guía, no regla absoluta).

## 2. Catálogo de patrones arquitectónicos permitidos

El `architect` elige el patrón según el caso concreto y **debe justificar la
elección en un ADR** (ver sección 6). No hay un patrón único obligatorio, pero
existe una preferencia por defecto:

**Preferencia por defecto: arquitectura modular** (monolito modular o
"modular monolith"), que permite escalar hacia microservicios más adelante
sin reescritura completa, manteniendo baja complejidad operativa inicial.

Patrones disponibles en el catálogo:
- **Monolito modular** (por defecto para proyectos nuevos de tamaño pequeño/medio)
- **Microservicios** (solo si se justifica según criterio de la sección 3)
- **Arquitectura hexagonal / Clean Architecture** (recomendado cuando se
  requiere alta testabilidad y aislamiento del dominio respecto de frameworks
  externos)
- **MVC** (aceptable para proyectos simples, especialmente frontend)
- **Event-driven architecture** (cuando hay necesidad real de desacoplar
  procesos asíncronos — ver sección 4)
- **CQRS** (solo para dominios con clara separación entre carga de
  lectura/escritura y necesidad de escalar ambas independientemente)

Cualquier patrón fuera de este catálogo requiere justificación explícita del
`architect` y aprobación del PM antes de adoptarse.

## 3. Criterio de decisión: monolito modular vs. microservicios

- **Por defecto → Monolito modular**: aplica a prototipos, MVPs, equipos
  pequeños, y cualquier proyecto sin requisitos explícitos de escalado
  independiente por dominio.
- **Se evalúa microservicios solo si** el PM indica explícitamente una o más
  de estas condiciones:
  - Necesidad de escalado independiente de un dominio específico bajo carga.
  - Equipos distribuidos grandes trabajando en paralelo sobre dominios distintos.
  - Requisito de despliegue independiente por servicio (releases desacoplados,
    distintos ciclos de vida).
- El `architect` debe documentar esta decisión en un ADR, incluso cuando se
  elige monolito modular por defecto (para dejar constancia de que se evaluó
  la alternativa).

## 4. Comunicación entre servicios/módulos

Basado en el stack real de referencia del PM (proyecto en curso que ya utiliza
múltiples mecanismos), se establece el siguiente catálogo con criterios de uso:

- **REST**: protocolo por defecto para comunicación cliente-servidor estándar
  y para integraciones simples con terceros.
- **GraphQL**: se usa cuando el frontend requiere flexibilidad de consulta
  (evitar over-fetching/under-fetching) o consume datos de múltiples fuentes
  agregadas en un solo endpoint.
- **gRPC**: reservado para comunicación interna entre servicios/microservicios
  donde el rendimiento y la tipificación estricta (protobuf) son prioritarios.
  No se expone directamente a clientes externos/frontend.
- **Mensajería asíncrona (eventos/colas)**: se usa cuando existe necesidad real
  de desacoplar procesos, procesar tareas en background, o notificar cambios
  de estado entre módulos/servicios sin acoplamiento síncrono directo.

El `architect` debe justificar en ADR cuál mecanismo aplica a cada
comunicación específica del proyecto, evitando usar todos los mecanismos
disponibles sin criterio (evitar complejidad accidental).

## 5. Manejo de errores — estándar global

- Nunca fallar en silencio: todo error capturado debe loggearse con contexto
  estructurado (timestamp, módulo, operación, identificador de request/traza
  si aplica).
- Usar excepciones tipadas/custom errors en vez de errores genéricos
  (`Error` genérico o excepciones sin clasificar), permitiendo distinguir
  errores de negocio, de validación, de infraestructura y de terceros.
- Nunca exponer stack traces, mensajes internos de base de datos, ni detalles
  de implementación al cliente en entornos de producción. Las respuestas de
  error al cliente deben ser controladas y sin fuga de información sensible.
- Todo error de infraestructura crítico (falla de conexión a BD, servicio
  externo caído, etc.) debe distinguirse claramente de errores de validación
  de negocio (ej. "email inválido"), tanto en el código como en el logging.
- `qa-reviewer` debe rechazar cualquier PR que capture errores sin loggear, o
  que use manejo de errores genérico donde corresponde uno tipado.

## 6. Architecture Decision Records (ADRs)

- Los ADRs redactados por `architect` se almacenan **dentro del proyecto
  destino** (no dentro de `.opencode/`), en la ruta `docs/adr/`, con
  nomenclatura secuencial: `0001-titulo-decision.md`, `0002-...`, etc.
- **Plantilla obligatoria de ADR**:
ADR-000X: [Título de la decisión]
Estado
[Propuesto | Aceptado | Rechazado | Reemplazado por ADR-XXXX]

Contexto
[Qué problema o necesidad motiva esta decisión. Qué restricciones existen.]

Decisión
[Qué se decidió hacer, de forma clara y concreta.]

Alternativas consideradas
[Qué otras opciones se evaluaron y por qué no se eligieron.]

Consecuencias
[Qué implicaciones tiene esta decisión, positivas y negativas, a corto y

largo plazo. Qué queda más fácil y qué queda más difícil después de esto.]


- Todo ADR debe crearse **antes** de que `tech-lead` descomponga la tarea en
  `specs/01-planning.md`, cuando la decisión afecta la estructura del proyecto.
