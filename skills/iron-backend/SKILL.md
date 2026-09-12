---
name: iron-backend
description: Activate when implementing server logic, APIs, data access, migrations or backend tests from an approved spec and API contract, and you need to propose the change as a diff via nion-cli. Assumes agentes/backend-dev.md is already loaded for identity and rules.
---

# IRON Backend — Skill de herramienta (nion-cli)

Esta skill **no redefine** identidad, alcance ni reglas del rol — eso vive
en `agentes/backend-dev.md` (fuente canónica, cargar siempre primero).
Esta skill agrega únicamente el **procedimiento operativo** para proponer y
verificar cambios de código a través de `nion-cli`.

## Cuándo se activa

- Ya existe un spec aprobado (y contrato API si la feature toca frontend).
- El plan de implementación fue aprobado por el PM (ver
  `agentes/backend-dev.md`, sección 3, paso 3).
- Necesitás **proponer un diff concreto**, no solo discutir el enfoque.

## Superpoder: proponer un cambio vía nion-cli

Seguís el contrato definido en `context/tech-stack.md`, sección 1.1
("Frontend-Dev / Backend-Dev"). Resumen operativo:

1. Formateás el cambio como **diff unificado** (`git diff` style) para
   archivos existentes, o como **bloque de código con ruta explícita**
   para archivos nuevos o migraciones.
2. Junto al diff, indicás siempre:
   - Archivo destino (ruta completa).
   - Motivo (criterio de aceptación del spec que resuelve).
   - Comando de verificación sugerido (test, migración), si aplica.
   - Si es una migración de schema: dependencia explícita de orden (ej.
     "debe aplicarse antes que el endpoint X").
3. Proponés el diff a `nion-cli` y **esperás confirmación explícita**
   (`[Y/n]`) antes de asumir que se aplicó. Nunca tratás un cambio como
   `KNOWN` sin la salida real de `nion-cli` (ver
   `context/constraints.md`, sección 10.2).
4. Si `nion-cli` no está confirmado como funcional en este entorno
   (ver `context/tech-stack.md`, sección 1.1, "Estado de implementación"),
   marcás el resultado del paso 3 como `REQUIRES_VERIFICATION` y lo
   señalás explícitamente al PM, en vez de asumir que el diff se aplicó.

## Chequeo previo obligatorio: security-triggers

Antes de proponer un diff que toque autenticación, datos sensibles,
criptografía o endpoints públicos, verificás si el código coincide con
algún patrón de `context/security-triggers.yaml`. Si hay coincidencia, lo
señalás explícitamente en la propuesta (no bloquea tu trabajo, pero
`tech-lead` debe saberlo para priorizar la revisión de `cybersecurity`
quien, de todas formas, revisará el módulo completo más adelante — ver
`agentes/cybersecurity.md`, sección 2, "Regla base: activación
garantizada").

## Formato de propuesta (referencia rápida)

    ## Propuesta de cambio — <nombre archivo/endpoint>

    **Archivo**: src/api/<nombre>.ts (nuevo | modificado)
    **Motivo**: Resuelve criterio de aceptación N del spec <ruta>
    **Dependencia de orden**: (ej. "requiere migración 003 aplicada antes")
    **Comando de verificación sugerido**: npm test -- <nombre>.test.ts
    **Coincidencia con security-triggers.yaml**: Sí/No — patrones: [...]

```diff
    <diff unificado o bloque de código nuevo>
```

    ¿Confirmás la aplicación de este cambio? [Y/n]

No existe un `templates/` separado para esta skill, por el mismo motivo que
`iron-frontend`: el formato es corto y vive directamente aquí.

## Qué NO hace esta skill

- No decide alcance ni criterios de aceptación (eso es Tech-Lead).
- No aprueba su propio código (eso es QA).
- No decide si un hallazgo de security-triggers es una vulnerabilidad real
  (eso es Cybersecurity) — solo lo señala como dato para priorización.
- No aplica el diff sin confirmación del PM, bajo ninguna circunstancia.
- No repite los principios no negociables de transacciones, formato de
  error, rate limiting, validación de inputs o idempotencia — están en
  `agentes/backend-dev.md`, sección 6, y siguen aplicando íntegramente.
