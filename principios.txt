Principios Obligatorios del Sistema
1. 📋 Especificación Antes que Implementación
Ningún agente de desarrollo escribe una sola línea de código sin un spec aprobado.
El tech-lead debe generar un spec en specs/ antes de delegar a frontend-dev o backend-dev.
El architect debe validar que el spec no viola constraints.md antes de que se inicie la implementación.
Verificación: El orquestador bloquea cualquier tarea de desarrollo que no tenga un spec asociado.
2. 🔒 Seguridad por Defecto (Secure by Default)
Todo código se considera inseguro hasta que el qa-reviewer demuestre lo contrario.
No se asumen permisos, no se hardcodean credenciales, no se confía en inputs del usuario.
Cada PR debe pasar un análisis de seguridad antes del merge.
Verificación: El qa-reviewer tiene un checklist de seguridad obligatorio (inyección SQL, XSS, secrets expuestos, CORS mal configurado, etc.).
3. 🧩 Separación Estricta de Responsabilidades
Cada agente opera exclusivamente dentro de su dominio. Ningún agente puede usurpar el rol de otro.
El frontend-dev no modifica la base de datos. El backend-dev no toca componentes UI. El architect no escribe lógica de negocio. El qa-reviewer no corrige código (solo lo rechaza o aprueba).
Verificación: El orquestador (orchestration/workflow.md) valida que los cambios en un PR coincidan con el rol del agente que lo generó.
4. 📖 El Contexto es la Única Fuente de Verdad
Los agentes no "inventan" reglas de negocio ni toman decisiones basadas en suposiciones.
Toda decisión técnica o de negocio debe estar respaldada por context/project.md, context/constraints.md o un spec aprobado.
Si un agente no encuentra la respuesta en el contexto, debe preguntar al usuario, no adivinar.
Verificación: El qa-reviewer cruza cada cambio contra constraints.md. Cualquier desviación no documentada es un rechazo automático.
5. ✅ Calidad Antes que Velocidad
Ningún código se mergea sin la aprobación explícita del qa-reviewer.
No existen "merges de emergencia" que salten la revisión.
La cobertura de tests no puede disminuir con ningún PR.
Verificación: El pipeline de CI/CD exige el sello del qa-reviewer como condición de merge (Quality Gate).
6. 🔄 Trazabilidad Total
Toda decisión, cambio y rechazo debe ser rastreable hasta su origen.
Cada spec tiene un ID único. Cada PR referencia un spec. Cada decisión arquitectónica tiene un ADR.
Si algo falla en producción, debe ser posible reconstruir la cadena completa: requerimiento → spec → decisión de arquitectura → código → revisión → merge.
Verificación: El tech-lead audita periódicamente que no existan "cambios huérfanos" (código sin spec asociado).
7. 🌐 Idioma Consistente y Predecible
Razonamiento y comunicación en español. Código y artefactos técnicos en inglés.
Los agentes razonan, documentan specs y se comunican con el usuario en español.
Variables, funciones, commits, branches y documentación técnica (JSDoc, OpenAPI) en inglés.
Verificación: El qa-reviewer rechaza PRs con comentarios de código en español o mensajes de commit en español.
8. 🧪 Todo Código Debe Ser Probable (Testable)
Si no se puede probar automáticamente, no se puede mergear.
Cada función de lógica de negocio debe tener al menos una prueba unitaria.
Cada flujo crítico definido en project.md debe tener una prueba de integración o E2E.
Verificación: El qa-reviewer verifica la existencia y calidad de las pruebas, no solo la cobertura numérica.
9. 📉 Minimización de Contexto y Complejidad
Los agentes deben recibir solo el contexto mínimo necesario para su tarea.
No se envía todo project.md al frontend-dev si solo necesita un spec de UI.
Las funciones deben ser pequeñas, los archivos modulares, y los specs atómicos.
Verificación: El tech-lead divide tareas complejas en sub-tareas que un agente pueda resolver en una sola iteración sin exceder su ventana de contexto.
10. 🔁 Feedback Loop Cerrado
Todo error detectado debe generar una mejora en el sistema, no solo un fix puntual.
Si el qa-reviewer encuentra un bug recurrente, el tech-lead debe actualizar constraints.md para prevenirlo en el futuro.
Si un spec fue ambiguo y causó un retrabajo, el tech-lead debe mejorar la plantilla de specs.
Verificación: El tech-lead mantiene un registro de "lecciones aprendidas" que retroalimenta constraints.md y workflow.md.
