# Convención de Skills — IRON

## Propósito

Este archivo define cómo se organizan y usan las skills en IRON. Su diseño
está inspirado en cómo un asistente de IA con soporte nativo de skills
(carpeta + archivo de entrada fijo) las consume, para que, si en el futuro
IRON migra a un motor con lectura automática de skills (ver
`orchestration/nion-cli-api.md`, DISEÑO FUTURO), la estructura ya sea
compatible sin necesitar reescritura.

**Estado actual (KNOWN)**: no existe todavía un motor automático que
recorra `skills/` por su cuenta. La lectura es **manual**: cada agente,
al activarse, debe abrir su propia carpeta (`skills/iron-<rol>/SKILL.md`)
como parte de su procedimiento, igual que hoy carga `agentes/<rol>.md`.
Ver `context/tech-stack.md`, sección 1.1, para el contrato de herramienta
vigente.

## Estructura obligatoria
skills/
├── README.md ← este archivo
├── iron-<rol>/
│   ├── SKILL.md ← punto de entrada obligatorio, siempre este nombre
│   ├── templates/ ← opcional, solo si el rol tiene formatos propios
│   │   └── <nombre>-format.md
│   └── scripts/ ← opcional, solo si el rol tiene comandos propios repetibles
│       └── <nombre>.sh

## Reglas de contenido

1. **`SKILL.md` es un router, no un contenedor de todo.**
   Debe incluir, al inicio, un bloque de metadatos igual al usado
   originalmente en este proyecto:

       ---
       name: iron-<rol>
       description: <cuándo se activa esta skill, en una o dos frases>
       ---

   Seguido de una lista breve de **qué operaciones habilita** (el
   "superpoder" concreto: qué comando de `nion-cli` propone, qué formato
   usa, qué hace con la salida). El detalle extenso va en archivos
   separados dentro de la misma carpeta, referenciados por ruta relativa.

2. **Nada se duplica. Todo contenido tiene un único dueño.**
   Antes de agregar un archivo a `templates/` o `scripts/` de una skill,
   verificar si ese contenido ya vive en otro lugar de IRON
   (`context/constraints.md`, `context/architecture.md`, otro `SKILL.md`).
   Si ya existe, se **referencia por ruta**, nunca se copia.

   Tabla de dueños ya establecida (ampliar aquí a medida que se agreguen
   nuevas skills):

   | Contenido | Dueño canónico | Ruta |
   |---|---|---|
   | Formato de veredicto de QA | `iron-qa` | `skills/iron-qa/templates/veredicto-format.md` |
   | Formato de reporte de Cybersecurity | `iron-cyber` | `skills/iron-cyber/templates/reporte-format.md` |
   | Plantilla de spec | `iron-tech-lead` | `skills/iron-tech-lead/templates/spec-template.md` |
   | Checklist DoD | `context/constraints.md` (no es una skill) | Referenciado, nunca copiado |
   | Estados de conocimiento (KNOWN/INFERRED/UNKNOWN/REQUIRES_VERIFICATION) | `context/constraints.md` sección 10.2 | Referenciado, nunca copiado |
   | `security-triggers.yaml` | `context/` (no es una skill) | Referenciado desde `iron-qa` e `iron-cyber`, nunca copiado |

3. **Solo contenido exclusivo de un rol vive dentro de su carpeta de skill.**
   Si dos o más roles necesitan el mismo contenido, ese contenido no es
   "de una skill" — pertenece a `context/` o `agentes/`, y las skills que
   lo necesiten lo citan por ruta.

4. **Identidad y reglas de negocio del rol NO viven en la skill.**
   Eso sigue siendo responsabilidad exclusiva de `agentes/<rol>.md`
   (fuente canónica de identidad, alcance y reglas duras — ver decisión
   de Fase 1 de esta auditoría). La skill solo añade el **procedimiento
   operativo de herramienta** sobre esa identidad ya definida.

## Qué evitar (lecciones de la versión anterior)

- No recrear archivos `SKILL.md` que resuman de memoria las reglas de
  `agentes/<rol>.md` — eso fue lo que causó divergencia y pérdida de
  reglas críticas (ej. la "Regla de Oro" de Tech-Lead quedó ausente del
  skill anterior). El `SKILL.md` nuevo asume que `agentes/<rol>.md` ya fue
  cargado y no repite su contenido.
- No crear una carpeta `scripts/roles/` paralela con una segunda copia en
  inglés. Si se necesita una versión resumida para otro fin, se referencia
  la misma fuente, no se reescribe.