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
import fnmatch
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

IGNORAR_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".iron_mapa"}

# Patrones de archivos que NUNCA se mapean, ni siquiera con hash — evita que
# el mapa confirme la existencia/tamaño de secretos (ver Fase de auditoría,
# hallazgo sobre .env/cookies en un proyecto real).
EXCLUIR_ARCHIVOS = [
    "*.env", "*.env.*",           # .env, variables.env, .env.local, etc.
    "*cookies*",
    "*.pem", "*.key", "*.p12", "*.pfx",
    "*credentials*", "*secret*",
]

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
        if any(fnmatch.fnmatch(ruta.name, patron) for patron in EXCLUIR_ARCHIVOS):
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

    ahora = datetime.now(timezone.utc)
    mapa = {
        "generado_en": ahora.isoformat(timespec="seconds"),
        "archivos": archivos,
    }

    destino_dir = raiz / ".iron_mapa"
    destino_dir.mkdir(exist_ok=True)

    # Versionado por fecha: cada corrida queda como un archivo aparte, para
    # que el usuario pueda ver cuál mapa es más reciente y comparar contra
    # el anterior si hace falta. mapa_completo.json (sin fecha) siempre
    # apunta al último, para que herramientas que esperan un nombre fijo
    # (ej. el comando 'm' del .bashrc, o context/tech-stack.md consumidores
    # futuros) sigan funcionando sin cambios.
    etiqueta_fecha = ahora.strftime("%Y%m%d-%H%M%S")
    destino_versionado = destino_dir / f"mapa_completo-{etiqueta_fecha}.json"
    destino_estable = destino_dir / "mapa_completo.json"

    contenido_json = json.dumps(mapa, indent=2, ensure_ascii=False)
    destino_versionado.write_text(contenido_json)
    destino_estable.write_text(contenido_json)

    _rotar_mapas_viejos(destino_dir)

    return {"success": True, "path": str(destino_versionado), "archivos_mapeados": len(archivos),
             "message": f"Mapa generado con {len(archivos)} archivos ({etiqueta_fecha})"}


def _rotar_mapas_viejos(destino_dir, max_versiones=2):
    """Conserva solo los `max_versiones` mapas versionados más recientes.

    El formato de nombre (mapa_completo-AAAAMMDD-HHMMSS.json) ordena
    correctamente por fecha con un simple sort de strings, sin necesidad de
    parsear cada nombre.
    """
    versionados = sorted(destino_dir.glob("mapa_completo-*.json"), reverse=True)
    for viejo in versionados[max_versiones:]:
        viejo.unlink()
