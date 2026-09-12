"""Punto de entrada único de iron_ops.

Traduce los argumentos de línea de comandos (usados por los alias de
.bashrc: crear/clonar/ir/mapa/listar) en llamadas al Project Service, e
imprime siempre un JSON por stdout.

El exit code solo distingue "el script mismo falló" (1) de "la operación
reportó un resultado de negocio" (0, incluso si ese resultado es un error
controlado como 'not_found' o 'already_exists') — así un typo de usuario
nunca mata la sesión de shell, a diferencia de lo que hacía el _bashrc
original con sus `exit` dentro de funciones.
"""

import json
import sys

from . import project_mapper, project_service


def _ejecutar(accion, args):
    if accion == "crear":
        return project_service.create_project(args[0])
    if accion == "clonar":
        return project_service.clone_project(args[0], args[1] if len(args) > 1 else None)
    if accion == "ir":
        return project_service.switch_project(args[0])
    if accion == "listar":
        return {"success": True, "projects": project_service.list_projects()}
    if accion == "activo":
        activo = project_service.get_active_project()
        return {"success": activo is not None, "project": activo,
                 "message": "sin proyecto activo" if activo is None else None}
    if accion == "mapa":
        activo = project_service.get_active_project()
        if not activo:
            return {"success": False, "message": "no hay proyecto activo — usá 'ir <proyecto>' primero"}
        return project_mapper.generar_mapa(activo["path"])

    return {"success": False, "error_type": "unknown_action",
             "message": f"acción desconocida: '{accion}' (usar: crear|clonar|ir|listar|activo|mapa)"}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "message": "uso: iron-ops <crear|clonar|ir|listar|activo|mapa> [args]"}))
        sys.exit(1)

    accion, args = sys.argv[1], sys.argv[2:]

    try:
        resultado = _ejecutar(accion, args)
    except project_service.ProjectServiceError as e:
        resultado = {"success": False, "error_type": "state_corrupted", "message": str(e)}
    except IndexError:
        resultado = {"success": False, "error_type": "missing_argument",
                     "message": f"faltan argumentos para '{accion}'"}

    print(json.dumps(resultado, ensure_ascii=False))


if __name__ == "__main__":
    main()
