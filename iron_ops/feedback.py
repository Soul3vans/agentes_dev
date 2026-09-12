"""Feedback Handler.

Normaliza el resultado de cualquier operación (Project Service o Execution
Service) en dos formas:
  - un mensaje breve para el usuario (incluye la corrección aplicada, si hubo);
  - un bloque de evidencia estructurada para que QA-Reviewer / Cybersecurity
    lo inserten en su formato de veredicto ya existente
    (agentes/qa-reviewer.md §3, agentes/cybersecurity.md §6), etiquetado
    siempre como KNOWN por venir de una ejecución real.
"""


def mensaje_usuario(resultado):
    if resultado.get("success"):
        base = f"✅ {resultado.get('message', 'operación completada')}"
    else:
        base = f"⚠️ {resultado.get('message', 'la operación falló')}"

    correccion = resultado.get("correction_applied")
    if correccion:
        base += f"\n   (corregí automáticamente: '{correccion['original']}' → '{correccion['corregido']}')"

    return base


def evidencia_qa(resultado_ejecucion):
    """resultado_ejecucion: ExecutionResult devuelto por execution_service.run_test()."""
    return {
        "comando_ejecutado": " ".join(resultado_ejecucion.command),
        "exit_code": resultado_ejecucion.exit_code,
        "stdout": resultado_ejecucion.stdout,
        "stderr": resultado_ejecucion.stderr,
        "duracion_ms": resultado_ejecucion.duration_ms,
        "estado_conocimiento": "KNOWN",
    }
