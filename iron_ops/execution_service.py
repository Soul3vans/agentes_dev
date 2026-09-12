"""Execution Service.

Único punto del sistema que ejecuta procesos reales. Dos carriles:

  - run_workspace_command(): operaciones de proyecto (git clone, etc).
    Sin restricción de rol — cualquier keyword del usuario llega aquí.

  - run_test(): ejecución de tests. Solo acepta un argv YA VALIDADO por
    test_runners.validar_action() contra el catálogo de runners, y solo
    para los roles autorizados (qa-reviewer, cybersecurity).

Reglas duras (ver Fase 5 de la auditoría):
  1. Siempre argv en lista, nunca shell=True con texto interpolado.
  2. Timeout obligatorio en toda ejecución.
  3. El resultado siempre se devuelve estructurado, nunca se asume éxito.
"""

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

DEFAULT_TIMEOUT_S = 120


@dataclass
class ExecutionResult:
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: int
    command: list
    error_type: str = None


def _run(argv, cwd=None, timeout=DEFAULT_TIMEOUT_S):
    inicio = time.monotonic()
    try:
        proceso = subprocess.run(
            argv,
            cwd=cwd,
            timeout=timeout,
            capture_output=True,
            text=True,
            shell=False,  # nunca interpolar texto en un shell
        )
        duracion_ms = int((time.monotonic() - inicio) * 1000)
        return ExecutionResult(
            success=proceso.returncode == 0,
            exit_code=proceso.returncode,
            stdout=proceso.stdout,
            stderr=proceso.stderr,
            duration_ms=duracion_ms,
            command=argv,
        )
    except subprocess.TimeoutExpired:
        duracion_ms = int((time.monotonic() - inicio) * 1000)
        return ExecutionResult(
            success=False, exit_code=-1, stdout="", stderr=f"timeout tras {timeout}s",
            duration_ms=duracion_ms, command=argv, error_type="timeout",
        )
    except FileNotFoundError as e:
        return ExecutionResult(
            success=False, exit_code=-1, stdout="", stderr=str(e),
            duration_ms=0, command=argv, error_type="binary_not_found",
        )


def run_workspace_command(argv, cwd=None):
    """Carril A: crear/clonar y operaciones de proyecto. Sin restricción de rol."""
    return _run(argv, cwd=cwd)


def run_test(argv, cwd, allowed_roles, calling_role):
    """Carril B: ejecución de tests, restringido por rol.

    'argv' debe llegar ya validado por test_runners.validar_action() — este
    servicio no vuelve a interpretar flags ni rutas, solo verifica el rol
    llamante y ejecuta.
    """
    if calling_role not in allowed_roles:
        return ExecutionResult(
            success=False, exit_code=-1, stdout="",
            stderr=f"rol '{calling_role}' no autorizado para ejecutar tests (permitidos: {allowed_roles})",
            duration_ms=0, command=argv, error_type="unauthorized_role",
        )

    cwd_resuelto = str(Path(cwd).resolve())
    return _run(argv, cwd=cwd_resuelto)
