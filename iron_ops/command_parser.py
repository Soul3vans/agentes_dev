"""Command Parser / Validator.

Interpreta y corrige los argumentos de `crear`, `clonar` e `ir` ANTES de que
lleguen al Project Service. No ejecuta nada — solo valida y, cuando existe una
corrección de alta confianza, la propone.

Diseño (ver conversación de auditoría, Fase 4):
- clonar: valida sintaxis de URL git (ssh/https). Si detecta el error típico
  de owner/repo intercambiados alrededor de ':' y '/', corrige automáticamente.
  Si no hay corrección segura, devuelve (None, None) y quien llama debe pedir
  aclaración al usuario — nunca se adivina un repo distinto al que se quiso decir.
- ir: resuelve contra la lista REAL de proyectos existentes (nunca hardcodeada),
  usando distancia de similitud. Una sola coincidencia de alta confianza se
  corrige sola; varias coincidencias parecidas se reportan como ambiguas.
"""

import difflib
import re

_SSH_OK = re.compile(r"^git@(?P<host>[\w.\-]+):(?P<owner>[\w.\-]+)/(?P<repo>[\w.\-]+?)(\.git)?$")
_SSH_OWNER_REPO_SWAPPED = re.compile(
    r"^git@(?P<host>[\w.\-]+)/(?P<owner>[\w.\-]+):(?P<repo>[\w.\-]+?)(\.git)?$"
)
_HTTPS_OK = re.compile(r"^https://(?P<host>[\w.\-]+)/(?P<owner>[\w.\-]+)/(?P<repo>[\w.\-]+?)(\.git)?/?$")


def validate_and_correct_git_url(url_cruda):
    """Devuelve (url_final, correccion).

    correccion es None si la URL ya era válida.
    correccion es {"original": ..., "corregido": ...} si se aplicó un fix seguro.
    Devuelve (None, None) si no se pudo interpretar ni corregir con confianza.
    """
    url = url_cruda.strip()

    if _SSH_OK.match(url) or _HTTPS_OK.match(url):
        return url, None

    m = _SSH_OWNER_REPO_SWAPPED.match(url)
    if m:
        corregida = f"git@{m['host']}:{m['owner']}/{m['repo']}.git"
        return corregida, {"original": url, "corregido": corregida}

    return None, None


def repo_name_from_url(url):
    """Extrae un nombre de carpeta razonable a partir de la URL ya validada."""
    return re.sub(r"\.git$", "", url.rstrip("/").split("/")[-1])


def resolve_project_name(nombre_pedido, candidatos, umbral_alta_confianza=0.75):
    """Resuelve 'nombre_pedido' contra la lista real de proyectos existentes.

    Devuelve (elegido, hubo_correccion, ambiguos):
      - coincidencia clara y única  -> (nombre_real, True, None)
      - ninguna coincidencia razonable -> (None, False, None)
      - varias coincidencias parecidas -> (None, False, [lista_de_candidatos])
    """
    if not candidatos:
        return None, False, None

    coincidencias = difflib.get_close_matches(nombre_pedido, candidatos, n=3, cutoff=0.5)
    if not coincidencias:
        return None, False, None

    mejor = coincidencias[0]
    ratio_mejor = difflib.SequenceMatcher(None, nombre_pedido, mejor).ratio()

    hay_segunda_cercana = len(coincidencias) > 1 and (
        ratio_mejor - difflib.SequenceMatcher(None, nombre_pedido, coincidencias[1]).ratio() <= 0.15
    )

    if ratio_mejor >= umbral_alta_confianza and not hay_segunda_cercana:
        return mejor, True, None

    return None, False, coincidencias
