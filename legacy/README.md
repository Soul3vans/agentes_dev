# legacy/

Esta carpeta guarda artefactos del sistema anterior (`agente_sistema` /
`.bashrc` viejo de Termux) como **referencia histórica únicamente**.

Nada de lo que hay acá se ejecuta ni se carga como parte de `agentes_dev`.
El `.bashrc` real de la sesión de Termux vive en `~/.bashrc` (fuera de este
repo) y fue reescrito desde cero para invocar `iron_ops/` — ver
`orchestration/test-runners.yaml`, `scripts/iron-ops` y `skills/iron-project/`
para la implementación vigente.

## Contenido

- `bashrc-viejo-termux`: versión del `.bashrc` original del sistema
  `agente_sistema` (keywords `ir`/`np`/`clonar`/`q`/`ia`, mapa vía
  `.ia_mapa/`, agentes Python sueltos `agente_backend.py` etc.). Se conserva
  como referencia para auditar qué capacidades existían antes de la
  migración a IRON — no como fuente de verdad operativa.
