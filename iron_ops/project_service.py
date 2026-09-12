"""Project Service.

Fuente única de verdad sobre qué proyectos existen y cuál está activo.
Reemplaza el "proyecto activo = $PWD" implícito y volátil del sistema
anterior por un registro persistente (IRON_HOME/projects.json) que
sobrevive entre sesiones de Termux.

Distingue origen "created" vs "cloned" como metadato (no como regla física
obligatoria), preservando la separación PROYECTOS_DIR / GITHUB_DIR que ya
existía en agente_sistema.

Nunca compite con specs/00-status.md: este archivo es solo un índice de
proyectos, no el estado de contenido de ninguno de ellos.
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from . import command_parser
from .execution_service import run_workspace_command

IRON_HOME = Path(os.environ.get("IRON_HOME", os.path.expanduser("~/.iron")))
PROYECTOS_DIR = Path(os.environ.get("IRON_PROYECTOS_DIR", os.path.expanduser("~/agente_sistema/proyectos")))
GITHUB_DIR = Path(os.environ.get("IRON_GITHUB_DIR", os.path.expanduser("~/agente_sistema/github")))
STATE_FILE = IRON_HOME / "projects.json"


class ProjectServiceError(Exception):
    """Estado corrupto o inconsistente. Nunca se sobrescribe en silencio."""


def _ahora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _cargar_estado():
    if not STATE_FILE.exists():
        return {"active_project": None, "projects": {}}
    try:
        return json.loads(STATE_FILE.read_text())
    except json.JSONDecodeError as e:
        raise ProjectServiceError(f"{STATE_FILE} está corrupto ({e}); revisar manualmente antes de continuar")


def _guardar_estado(estado):
    IRON_HOME.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(estado, indent=2, ensure_ascii=False))
    tmp.replace(STATE_FILE)  # escritura atómica: nunca deja el JSON a medias


def list_projects():
    return _cargar_estado()["projects"]


def get_active_project():
    estado = _cargar_estado()
    nombre = estado["active_project"]
    if not nombre:
        return None
    return {"name": nombre, **estado["projects"][nombre]}


def _registrar(nombre, ruta, origen, repo=None, branch=None):
    estado = _cargar_estado()
    existente = estado["projects"].get(nombre, {})
    estado["projects"][nombre] = {
        "path": str(ruta),
        "origin": origen,
        "repo": repo,
        "branch": branch,
        "created_at": existente.get("created_at", _ahora()),
        "last_active": _ahora(),
    }
    estado["active_project"] = nombre
    _guardar_estado(estado)


def create_project(nombre_pedido):
    slug = re.sub(r"[^a-zA-Z0-9_-]", "-", nombre_pedido).strip("-")
    if not slug:
        return {"success": False, "error_type": "invalid_name",
                 "message": f"'{nombre_pedido}' no es un nombre de proyecto válido"}

    destino = PROYECTOS_DIR / slug
    if destino.exists():
        return {"success": False, "error_type": "already_exists",
                 "message": f"Ya existe un proyecto en {destino}"}

    destino.mkdir(parents=True)
    _registrar(slug, destino, origen="created")
    return {"success": True, "name": slug, "path": str(destino),
             "message": f"Proyecto '{slug}' creado y activado"}


def clone_project(url_cruda, nombre=None):
    corregida, correccion = command_parser.validate_and_correct_git_url(url_cruda)
    if corregida is None:
        return {"success": False, "error_type": "unparseable_url",
                 "message": f"No pude interpretar '{url_cruda}' como repositorio git. "
                             "Formato esperado: git@host:owner/repo.git",
                 "correction_applied": None}

    slug = nombre or command_parser.repo_name_from_url(corregida)
    destino = GITHUB_DIR / slug
    if destino.exists():
        return {"success": False, "error_type": "already_exists",
                 "message": f"Ya existe un proyecto en {destino}", "correction_applied": correccion}

    GITHUB_DIR.mkdir(parents=True, exist_ok=True)
    resultado = run_workspace_command(["git", "clone", corregida, str(destino)])
    if not resultado.success:
        return {"success": False, "error_type": "git_clone_failed",
                 "message": resultado.stderr.strip() or "git clone falló",
                 "correction_applied": correccion, "command_executed": resultado.command}

    _registrar(slug, destino, origen="cloned", repo=corregida)
    return {"success": True, "name": slug, "path": str(destino),
             "correction_applied": correccion, "command_executed": resultado.command,
             "message": f"Proyecto '{slug}' clonado y activado"}


def switch_project(nombre_pedido):
    estado = _cargar_estado()
    candidatos = list(estado["projects"].keys())

    if nombre_pedido in candidatos:
        elegido, hubo_correccion = nombre_pedido, False
    else:
        elegido, hubo_correccion, ambiguos = command_parser.resolve_project_name(nombre_pedido, candidatos)
        if ambiguos:
            return {"success": False, "error_type": "ambiguous",
                     "message": f"'{nombre_pedido}' coincide con varios proyectos: {', '.join(ambiguos)}. Especificá cuál.",
                     "candidates": ambiguos}
        if elegido is None:
            return {"success": False, "error_type": "not_found",
                     "message": f"No encontré ningún proyecto parecido a '{nombre_pedido}'"}

    info = estado["projects"][elegido]
    estado["active_project"] = elegido
    info["last_active"] = _ahora()
    _guardar_estado(estado)

    return {"success": True, "name": elegido, "path": info["path"],
             "correction_applied": {"original": nombre_pedido, "corregido": elegido} if hubo_correccion else None,
             "message": f"Proyecto activo: '{elegido}'"}
