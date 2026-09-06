# CI Pipeline propuesta

> **Estado: DISEÑO FUTURO**  
> Este documento describe una visión de escalado.  
> **No forma parte del runtime actual** de IRON (1 modelo, ejecución secuencial).  
> El Orchestrator y los agentes **no deben cargarlo ni asumir** que las capacidades aquí descritas están disponibles.  
> Activación: solo cuando se migre formalmente a multi-worker / CI automatizada / API de nion-cli.

Objetivo: ejecutar tests, linters, SCA, y soportar despliegue canario; además integrar `nion-cli` para ejecutar comandos verificados y registrar salidas como evidencia KNOWN.

1. Flujo general (GitHub Actions como ejemplo)

- `on: pull_request` / `push` a `main`/`release`
- Jobs:
  - `checkout`
  - `setup` (instalar dependencias según stack)
  - `lint` (eslint/flake8/others)
  - `test` (unit + integration)
  - `sast_sca` (npm audit / pip-audit / snyk / trivy)
  - `build` (opcional)
  - `canary_deploy` (solo en `main` con etiqueta `canary` o por job manual)
  - `notify_nion` (envía resultado a `nion-cli` o registra artefactos de evidencia)

2. Integración con `nion-cli`

- `nion-cli` expone comandos que pueden ejecutarse mediante la CI con la aprobación del PM. Para auditoría, todos los resultados (stdout/stderr, exit code) deben almacenarse como artefactos y referenciados en el handoff.
- En PRs, antes de aplicar un diff, `nion-cli` puede ejecutar `verify` scripts listados por el dev (p. ej. `npm run test:affected`) y adjuntar la salida al comentario del PR.

3. Ejemplo mínimo de `ci.yml` (esquema)

```yaml
name: CI
on: [pull_request, push]
jobs:
  checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup
        run: |
          # instalar dependencias según stack
      - name: Lint
        run: # linter command
      - name: Test
        run: # test command
      - name: SCA
        run: # npm audit / pip-audit etc.
      - name: Upload evidence
        uses: actions/upload-artifact@v4
        with:
          name: ci-evidence
          path: ./ci-evidence/
```

4. Canary deploy y rollback

- Usar feature flags o despliegue por etiquetas en infraestructura (k8s, lambda, etc.).
- Canary: desplegar a subset (10% tráfico), ejecutar smoke tests, observar métricas (error rate, latency, saturation). Si falla, activar rollback automático vía pipeline (`deploy --from-tag <previous>`).

5. Recomendaciones

- Conectar `nion-cli` con la CI para que acciones aprobadas por PM queden trazadas (ej. `nion-cli apply --pr 123`).
- Guardar artefactos de evidencia en cada job y referenciarlos en el handoff (`EVIDENCE: ci-evidence/<run-id>`).
- Exponer endpoints de comprobación desde `nion-cli` para que la CI pueda solicitar verificación previa (ver `nion-cli-api.md`).
