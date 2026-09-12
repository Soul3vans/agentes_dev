"""iron_ops — capa operativa de agentes_dev (Project Service, Command Parser,
Execution Service, catálogo de runners de test, Project Mapper y Feedback Handler).

Reemplaza la lógica dispersa y duplicada de _bashrc / _bashrc_proyectos /
_bashrc_ia_asistente / orquestador.py por una única implementación Python,
invocable tanto desde las keywords de shell (crear/clonar/ir/mapa) como
directamente por el Orchestrator y los agentes.
"""
