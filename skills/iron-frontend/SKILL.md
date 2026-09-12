---
name: iron-frontend
description: Activate when implementing UI, client state, accessibility or frontend tests from an approved spec and API contract, and you need to propose the change as a diff via nion-cli. Assumes agentes/frontend-dev.md is already loaded for identity and rules.
---

# IRON Frontend — Skill de herramienta (nion-cli)

Esta skill **no redefine** identidad, alcance ni reglas del rol — eso vive
en `agentes/frontend-dev.md` (fuente canónica, cargar siempre primero).
Esta skill agrega únicamente el **procedimiento operativo** para proponer y
verificar cambios de código a través de `nion-cli`.

## Cuándo se activa

- Ya existe un spec aprobado (y contrato API si la feature toca backend).
- El plan de implementación fue aprobado por el PM (ver
  `agentes/frontend-dev.md`, sección 3, paso 3).
- Necesitás **proponer un diff concreto**, no solo discutir el enfoque.

## Superpoder: proponer un cambio vía nion-cli

Seguís el contrato definido en `context/tech-stack.md`, sección 1.1
("Frontend-Dev / Backend-Dev"). Resumen operativo:

1. Formateás el cambio como **diff unificado** (`git diff` style) para
   archivos existentes, o como **bloque de código con ruta explícita**
   para archivos nuevos.
2. Junto al diff, indicás siempre:
   - Archivo destino (ruta completa).
   - Motivo (criterio de aceptación del spec que resuelve).
   - Comando de verificación sugerido (test/build), si aplica.
3. Proponés el diff a `nion-cli` y **esperás confirmación explícita**
   (`[Y/n]`) antes de asumir que se aplicó. Nunca tratás un cambio como
   `KNOWN` sin la salida real de `nion-cli` (ver
   `context/constraints.md`, sección 10.2).
4. Si `nion-cli` no está confirmado como funcional en este entorno
   (ver `context/tech-stack.md`, sección 1.1, "Estado de implementación"),
   marcás el resultado del paso 3 como `REQUIRES_VERIFICATION` y lo
   señalás explícitamente al PM, en vez de asumir que el diff se aplicó.

## Formato de propuesta (referencia rápida)

    ## Propuesta de cambio — <nombre archivo>

    **Archivo**: src/components/<Nombre>.tsx (nuevo | modificado)
    **Motivo**: Resuelve criterio de aceptación N del spec <ruta>
    **Comando de verificación sugerido**: npm test -- <Nombre>.test.tsx

```diff
    <diff unificado o bloque de código nuevo>
```

    ¿Confirmás la aplicación de este cambio? [Y/n]

No existe un `templates/` separado para esta skill: el formato de arriba es
lo suficientemente corto como para vivir directamente aquí, sin necesitar
un archivo aparte (a diferencia de QA/Cyber, que sí tienen formatos de
veredicto/reporte más extensos — ver sus propias skills).

## Qué NO hace esta skill

- No decide alcance ni criterios de aceptación (eso es Tech-Lead).
- No aprueba su propio código (eso es QA).
- No aplica el diff sin confirmación del PM, bajo ninguna circunstancia.
- No repite las reglas de accesibilidad, testing o estado global — están
  en `agentes/frontend-dev.md`, secciones 5 y 6, y siguen aplicando
  íntegramente.
