"""Project Mapper.

Genera .iron_mapa/mapa_completo.json: estructura del proyecto, archivos, hash,
y para cada archivo (según lenguaje) sus imports/clases/funciones principales.

Reemplaza las dos implementaciones divergentes que existían en agente_sistema
(_bashrc y _bashrc_ia_asistente) por una única fuente. Usa `ast` para Python
(más confiable que regex); para JS/TS usa una extracción liviana marcada
explícitamente como "no-AST" para no aparentar más precisión de la que tiene.

Es de solo lectura: entra en el Carril A (sin confirmación humana).
"""

import ast
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

IGNORAR_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".iron_mapa"}

CAPA_POR_EXTENSION = {
    ".py": "backend", ".go": "backend", ".java": "backend", ".rb": "backend",
    ".js": "frontend", ".jsx": "frontend", ".ts": "frontend", ".tsx": "frontend",
    ".vue": "frontend", ".html": "frontend", ".css": "frontend",
    ".sql": "database",
    ".yaml": "config", ".yml": "config", ".json": "config", ".env": "config",
}

_RE_CLASE_JS = re.compile(r"^\s*(?:export\s+)?class\s+(\w+)", re.MULTILINE)
_RE_FUNCION_JS = re.compile(r"^\s*(?:export\s+)?function\s+(\w+)", re.MULTILINE)


def _hash_archivo(ruta):
    return "sha1:" + hashlib.sha1(ruta.read_bytes()).hexdigest()


def _analizar_python(contenido):
    try:
        arbol = ast.parse(contenido)
    except SyntaxError:
        return {"imports": [], "clases": [], "funciones": [], "nota": "no se pudo parsear (SyntaxError)"}

    imports, clases, funciones = [], [], []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            imports.extend(alias.name for alias in nodo.names)
        elif isinstance(nodo, ast.ImportFrom) and nodo.module:
            imports.append(nodo.module)
        elif isinstance(nodo, ast.ClassDef):
            clases.append(nodo.name)
        elif isinstance(nodo, ast.FunctionDef):
            funciones.append(nodo.name)

    return {"imports": sorted(set(imports)), "clases": clases, "funciones": funciones}


def _analizar_js_like(contenido):
    return {
        "clases": _RE_CLASE_JS.findall(contenido),
        "funciones": _RE_FUNCION_JS.findall(contenido),
        "nota": "extracción por regex, no AST — puede omitir casos",
    }


def generar_mapa(project_root):
    raiz = Path(project_root)
    archivos = []

    for ruta in raiz.rglob("*"):
        if not ruta.is_file() or any(parte in IGNORAR_DIRS for parte in ruta.parts):
            continue
        try:
            contenido = ruta.read_text(errors="ignore")
        except OSError:
            continue

        extension = ruta.suffix
        entrada = {
            "ruta": str(ruta.relative_to(raiz)),
            "hash": _hash_archivo(ruta),
            "lineas": contenido.count("\n") + 1,
            "capa": CAPA_POR_EXTENSION.get(extension, "otro"),
        }

        if extension == ".py":
            entrada.update(_analizar_python(contenido))
        elif extension in (".js", ".jsx", ".ts", ".tsx"):
            entrada.update(_analizar_js_like(contenido))

        archivos.append(entrada)

    mapa = {
        "generado_en": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "archivos": archivos,
    }

    destino_dir = raiz / ".iron_mapa"
    destino_dir.mkdir(exist_ok=True)
    destino = destino_dir / "mapa_completo.json"
    destino.write_text(json.dumps(mapa, indent=2, ensure_ascii=False))

    return {"success": True, "path": str(destino), "archivos_mapeados": len(archivos),
             "message": f"Mapa generado con {len(archivos)} archivos"}
