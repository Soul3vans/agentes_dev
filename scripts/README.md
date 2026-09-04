# IRON Scripts Wrapper (Termux / nion-cli)

Evita copiar y pegar prompts. Cada comando carga solo el rol necesario.

## Instalación rápida en Termux

```bash
# 1. Copia esta carpeta scripts/ a tu teléfono (o clona el repo)
# 2. Dale permisos
chmod +x scripts/iron scripts/iron-*

# 3. (Opcional) Añade al PATH
export PATH="$PATH:$HOME/ruta/a/agentes_dev/scripts"
```

## Uso

```bash
# Forma completa
iron <rol> "tu solicitud"

# Atajos
iron-orch   "Quiero agregar login con email"
iron-tl     "Convierte esto en un spec: ..."
iron-intake  "Como usuario quiero recuperar mi contraseña"
iron-arch   "Necesito decidir cómo escalar el módulo de pagos"
iron-be     "Implementa el endpoint según el spec 002"
iron-fe     "Implementa la pantalla de reset password"
iron-qa     "Revisa el módulo de autenticación"
iron-cyber  "Audita el manejo de tokens"
```

## Roles disponibles

| Comando     | Rol            |
|-------------|----------------|
| iron-orch   | Orchestrator   |
| iron-tl     | Tech-Lead      |
| iron-arch   | Architect      |
| iron-be     | Backend-Dev    |
| iron-fe     | Frontend-Dev   |
| iron-qa     | QA-Reviewer    |
| iron-cyber  | Cybersecurity  |
| iron-intake | Intake → Spec  |

## Configuración (opcional)

```bash
export IRON_PROVIDER=ollama          # default
export IRON_MODEL=qwen2.5-coder      # default
```

## Flujo típico

1. `iron-orch "quiero X"`     → clasifica y dice a quién delegar
2. `iron-intake "historia..."` → genera el spec
3. `iron-tl "..."`            → confirma/ajusta spec y contratos
4. `iron-be` / `iron-fe`      → implementan
5. `iron-qa` → `iron-cyber`   → validan
