"""Catálogo de runners de test.

Carga orchestation/test-runners.yaml (base, del framework) y
context/test-runners.override.yaml (si existe en el proyecto activo, se
fusiona por campo 'stack'), y valida las Action que QA-Reviewer y
Cybersecurity proponen para el Carril B del Execution Service.

Nunca deja pasar un stack, target_path o flag que no esté explícitamente
en el catálogo — ver Fase 4 y 5 de la auditoría.
"""

import fnmatch
import os
from pathlib import Path

import yaml  # requiere PyYAML: pip install pyyaml --break-system-packages

# iron_ops/ vive directamente dentro de agentes_dev/, así que por defecto el
# catálogo base se busca un nivel arriba de este archivo — nunca depende de
# desde qué carpeta se haya invocado la keyword. IRON_FRAMEWORK_DIR permite
# sobreescribirlo si el paquete se instala en otro lado.
IRON_FRAMEWORK_DIR = Path(os.environ.get("IRON_FRAMEWORK_DIR", Path(__file__).resolve().parent.parent))
BASE_CATALOG_PATH = IRON_FRAMEWORK_DIR / "orchestation" / "test-runners.yaml"
ALLOWED_ROLES = ["qa-reviewer", "cybersecurity"]


def _cargar_yaml(path):
    if not path.exists():
        return {}
    contenido = yaml.safe_load(path.read_text())
    return contenido or {}


def cargar_catalogo(project_root):
    """Fusiona catálogo base + override del proyecto, por campo 'stack'."""
    base = _cargar_yaml(BASE_CATALOG_PATH)
    runners = {r["stack"]: r for r in base.get("runners", [])}

    override_path = Path(project_root) / "context" / "test-runners.override.yaml"
    override = _cargar_yaml(override_path)
    for entrada in override.get("overrides", []):
        stack = entrada["stack"]
        runners[stack] = {**runners.get(stack, {}), **entrada}

    return runners


def validar_action(action, project_root):
    """action = {"stack": ..., "target_path": ..., "flags": [...]}.

    Devuelve (argv, error). argv es None si la validación falla, en cuyo
    caso 'error' describe por qué — la Action nunca llega al Execution
    Service si algo no está en el catálogo.
    """
    catalogo = cargar_catalogo(project_root)
    stack = action.get("stack")
    if stack not in catalogo:
        return None, f"stack '{stack}' no está en el catálogo de runners"

    regla = catalogo[stack]
    raiz = Path(project_root).resolve()

    target = action.get("target_path", "")
    ruta_absoluta = (raiz / target).resolve()
    if raiz not in ruta_absoluta.parents and ruta_absoluta != raiz:
        return None, f"target_path '{target}' se sale del proyecto"
    if not fnmatch.fnmatch(target, regla.get("target_pattern", "")):
        return None, f"target_path '{target}' no coincide con el patrón permitido ({regla.get('target_pattern')})"

    flags_pedidos = action.get("flags") or regla.get("default_flags", [])
    permitidos = set(regla.get("allowed_flags", []))
    no_autorizados = [f for f in flags_pedidos if f not in permitidos]
    if no_autorizados:
        return None, f"flags no autorizados: {no_autorizados}"

    argv = regla["runner"].split() + [str(ruta_absoluta)] + list(flags_pedidos)
    return argv, None
