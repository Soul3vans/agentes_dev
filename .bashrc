# ============================================
# .BASHRC - SISTEMA IA ASISTENTE + AGENTES
# Termux / Xiaomi Redmi Note 11 (4GB RAM)
# ============================================

export ANDROID_API_LEVEL=$(getprop ro.build.version.sdk)

# ============================================
# VARIABLES GLOBALES
# ============================================

export AGENTE_HOME="$HOME/agente_sistema"
export PROYECTOS_DIR="$AGENTE_HOME/proyectos"
export GITHUB_DIR="$AGENTE_HOME/github"

# Asegurar directorios
mkdir -p "$PROYECTOS_DIR" 2>/dev/null
mkdir -p "$GITHUB_DIR" 2>/dev/null

# Alias rápido para coder
alias coder="ollama run qwen2.5-coder:1.5b"


# ============================================
# FUNCIÓN: CREAR MAPA DEL PROYECTO
# ============================================

crear_mapa_proyecto() {
    # Si no hay argumento, usar directorio actual
    if [ -z "$1" ]; then
        proyecto_path="$PWD"
    else
        proyecto_path="$1"
    fi

    # Verificar que existe
    if [ ! -d "$proyecto_path" ]; then
        echo "❌ Directorio no existe: $proyecto_path"
        return 1
    fi

    cd "$proyecto_path" || return 1

    echo "📁 Indexando: $(basename "$proyecto_path")"
    mkdir -p .ia_mapa

    python3 << 'PYSCRIPT'
import os
import json
import hashlib
from datetime import datetime

proyecto_path = os.getcwd()
mapa = {
    "proyecto": os.path.basename(proyecto_path),
    "creado": datetime.now().isoformat(),
    "ultimo_escaneo": datetime.now().isoformat(),
    "archivos": []
}

extensions = ('.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css',
              '.json', '.vue', '.go', '.java', '.sql', '.php')

for root, dirs, files in os.walk(proyecto_path):
    if '.ia_mapa' in dirs:
        dirs.remove('.ia_mapa')
    if '.git' in dirs:
        dirs.remove('.git')
    if 'node_modules' in dirs:
        dirs.remove('node_modules')
    if '__pycache__' in dirs:
        dirs.remove('__pycache__')

    for file in files:
        if file.endswith(extensions):
            ruta_completa = os.path.join(root, file)
            ruta_relativa = os.path.relpath(ruta_completa, proyecto_path)

            try:
                with open(ruta_completa, 'r', encoding='utf-8', errors='ignore') as f:
                    contenido = f.read()
                    lineas = len(contenido.splitlines())

                    imports = []
                    clases = []
                    for line in contenido.split('\n')[:50]:
                        if line.startswith(('import ', 'from ', 'require(', 'const ', 'function ', 'def ')):
                            if 'import' in line or 'require' in line:
                                imports.append(line.strip()[:60])
                            if line.startswith(('class ', 'def ', 'function ')):
                                clases.append(line.strip()[:60])

                    mapa["archivos"].append({
                        "ruta": ruta_relativa,
                        "lineas": lineas,
                        "hash": hashlib.md5(contenido.encode()).hexdigest(),
                        "imports": imports[:3],
                        "clases": clases[:3]
                    })
            except Exception:
                pass

with open(".ia_mapa/mapa_completo.json", "w") as f:
    json.dump(mapa, f, indent=2)

print(f"✅ {len(mapa['archivos'])} archivos indexados")
PYSCRIPT
}


# ============================================
# FUNCIÓN: DETECTAR TECNOLOGÍAS
# ============================================

detectar_tecnologias() {
    if [ -z "$1" ]; then
        cd "$PWD" || return 1
    else
        cd "$1" || return 1
    fi

    echo "🔍 Detectando tecnologías..."

    tecnologias=""

    # Backend
    ls *.py 2>/dev/null | grep -q . && tecnologias="$tecnologias Python"
    ls *.js 2>/dev/null | grep -q . && tecnologias="$tecnologias Node.js"
    ls *.go 2>/dev/null | grep -q . && tecnologias="$tecnologias Go"
    ls *.php 2>/dev/null | grep -q . && tecnologias="$tecnologias PHP"
    ls *.java 2>/dev/null | grep -q . && tecnologias="$tecnologias Java"

    # Frontend
    ls *.html 2>/dev/null | grep -q . && tecnologias="$tecnologias HTML"
    [ -f "package.json" ] && tecnologias="$tecnologias (npm)"
    [ -f "requirements.txt" ] && tecnologias="$tecnologias (pip)"
    [ -f "composer.json" ] && tecnologias="$tecnologias (composer)"
    [ -f "Gemfile" ] && tecnologias="$tecnologias (bundler)"

    # Frameworks específicos
    [ -f "package.json" ] && grep -q "react" package.json 2>/dev/null && tecnologias="$tecnologias React"
    [ -f "package.json" ] && grep -q "vue" package.json 2>/dev/null && tecnologias="$tecnologias Vue"
    [ -f "package.json" ] && grep -q "next" package.json 2>/dev/null && tecnologias="$tecnologias Next.js"
    [ -f "package.json" ] && grep -q "express" package.json 2>/dev/null && tecnologias="$tecnologias Express"
    [ -f "requirements.txt" ] && grep -q "django" requirements.txt 2>/dev/null && tecnologias="$tecnologias Django"
    [ -f "requirements.txt" ] && grep -q "flask" requirements.txt 2>/dev/null && tecnologias="$tecnologias Flask"
    [ -f "requirements.txt" ] && grep -q "fastapi" requirements.txt 2>/dev/null && tecnologias="$tecnologias FastAPI"

    # Base de datos
    ls *.sql 2>/dev/null | grep -q . && tecnologias="$tecnologias SQL"

    if [ -n "$tecnologias" ]; then
        echo "✅ Tecnologías detectadas: $tecnologias"
        mkdir -p .ia_mapa
        echo "{\"tecnologias\": \"$tecnologias\", \"fecha\": \"$(date -Iseconds)\"}" > .ia_mapa/tecnologias.json
    else
        echo "⚠️ No se detectaron tecnologías conocidas"
    fi
}


# ============================================
# FUNCIÓN: LISTAR PROYECTOS
# ============================================

listar_proyectos() {
    echo "📁 Proyectos locales (agentes):"
    if [ -d "$PROYECTOS_DIR" ]; then
        for d in "$PROYECTOS_DIR"/*/; do
            [ -d "$d" ] && echo "  🤖 $(basename "$d")"
        done
    else
        echo "  (ninguno)"
    fi

    echo ""
    echo "📦 Proyectos de GitHub:"
    if [ -d "$GITHUB_DIR" ]; then
        for d in "$GITHUB_DIR"/*/; do
            [ -d "$d" ] && echo "  📦 $(basename "$d")"
        done
    else
        echo "  (ninguno)"
    fi
}


# ============================================
# FUNCIÓN: IR A PROYECTO
# ============================================

ir() {
    if [ -z "$1" ]; then
        listar_proyectos
        return 1
    fi

    if [ -d "$PROYECTOS_DIR/$1" ]; then
        cd "$PROYECTOS_DIR/$1"
    elif [ -d "$GITHUB_DIR/$1" ]; then
        cd "$GITHUB_DIR/$1"
    else
        echo "❌ Proyecto '$1' no encontrado"
        echo ""
        listar_proyectos
        return 1
    fi

    echo "✅ En proyecto: $(basename "$PWD")"
    ls -la --color=auto 2>/dev/null | head -10
}


# ============================================
# FUNCIÓN: NUEVO PROYECTO
# ============================================

np() {
    if [ -z "$1" ]; then
        echo "Uso: np <nombre>"
        echo ""
        echo "Luego elige ubicación:"
        echo "  1) Proyecto local (agentes) - $PROYECTOS_DIR"
        echo "  2) Proyecto GitHub - $GITHUB_DIR"
        return 1
    fi

    nombre="$1"

    echo ""
    echo "¿Dónde quieres crear '$nombre'?"
    echo "  1) Proyecto local (para agentes)"
    echo "  2) Proyecto GitHub (para clonar después)"
    echo ""
    read -p "Elige (1/2): " ubicacion

    case $ubicacion in
        1)
            destino="$PROYECTOS_DIR/$nombre"
            mkdir -p "$destino"
            cd "$destino"
            crear_mapa_proyecto "$destino"
            echo "✅ Proyecto local creado en: $destino"
            ;;
        2)
            destino="$GITHUB_DIR/$nombre"
            mkdir -p "$destino"
            cd "$destino"
            crear_mapa_proyecto "$destino"
            echo "✅ Proyecto GitHub creado en: $destino"
            ;;
        *)
            echo "❌ Opción inválida"
            return 1
            ;;
    esac
}


# ============================================
# FUNCIÓN: CLONAR REPOSITORIO
# ============================================

clonar() {
    if [ -z "$1" ]; then
        echo "Uso: clonar <url> [nombre_destino]"
        echo ""
        echo "Ejemplos:"
        echo "  clonar https://github.com/usuario/repo.git"
        echo "  clonar git@github.com:usuario/repo.git"
        return 1
    fi

    url="$1"
    nombre="$2"

    if [ -z "$nombre" ]; then
        nombre=$(basename "$url" .git)
    fi

    destino="$GITHUB_DIR/$nombre"

    if [ -d "$destino" ]; then
        echo "❌ El proyecto '$nombre' ya existe en $destino"
        echo "   Usa: ir $nombre"
        return 1
    fi

    echo "📦 Clonando: $url"
    echo "📁 Destino: $destino"

    git clone "$url" "$destino"

    if [ $? -eq 0 ]; then
        echo "✅ Clonado correctamente"
        cd "$destino"
        crear_mapa_proyecto "$destino"
        detectar_tecnologias "$destino"
        echo ""
        echo "✅ Proyecto listo. Usa: ir $nombre"
    else
        echo "❌ Error al clonar"
        echo ""
        echo "💡 Si el repo es privado:"
        echo "   git config --global credential.helper store"
        echo "   Usa SSH: clonar git@github.com:usuario/repo.git"
        return 1
    fi
}


# ============================================
# FUNCIÓN: ACTUALIZAR REPOSITORIO
# ============================================

actualizar() {
    if [ ! -d .git ]; then
        echo "❌ No estás en un repositorio Git"
        return 1
    fi

    echo "📦 Actualizando repositorio..."
    echo "📊 Rama: $(git branch --show-current)"
    echo ""

    git pull

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Repositorio actualizado"
        echo "🔄 Actualizando mapa de IA..."
        crear_mapa_proyecto "$PWD"
        echo ""
        echo "✅ Todo actualizado"
    else
        echo "❌ Error al actualizar"
        return 1
    fi
}


# ============================================
# FUNCIÓN: COMMIT RÁPIDO
# ============================================

commit() {
    if [ ! -d .git ]; then
        echo "❌ No estás en un repositorio Git"
        return 1
    fi

    if [ -z "$1" ]; then
        echo "📝 Escribe el mensaje del commit:"
        read -r mensaje
    else
        mensaje="$*"
    fi

    if [ -z "$(git status --porcelain)" ]; then
        echo "⚠️ No hay cambios para commitear"
        return 1
    fi

    echo ""
    echo "📊 Cambios detectados:"
    git status --short
    echo ""

    read -p "¿Agregar todo y commitear? (s/n): " respuesta

    if [ "$respuesta" = "s" ]; then
        git add -A
        git commit -m "$mensaje"
        echo ""
        echo "✅ Commit realizado"
        echo "   Luego usa: git push"
        git log --oneline -1
    else
        echo "❌ Cancelado"
    fi
}


# ============================================
# FUNCIONES DE IA (preguntar)
# ============================================

# q - Preguntar sobre el proyecto actual
q() {
    if [ -f .ia_mapa/mapa_completo.json ]; then
        contexto=$(jq -r '.archivos[].ruta' .ia_mapa/mapa_completo.json 2>/dev/null | head -10)
        echo "Contexto: $contexto" | ollama run qwen2.5-coder:1.5b "$*"
    else
        ollama run qwen2.5-coder:1.5b "$*"
    fi
}

# qc - Preguntar sobre un archivo específico
qc() {
    if [ -z "$1" ]; then
        echo "Uso: qc <archivo> <pregunta>"
        echo "Ejemplo: qc app.py 'Qué hace esta función?'"
        return 1
    fi

    archivo="$1"
    shift
    pregunta="$*"

    if [ ! -f "$archivo" ]; then
        echo "❌ Archivo no encontrado: $archivo"
        return 1
    fi

    echo "📄 Analizando: $archivo"
    echo "🤔 Pregunta: $pregunta"
    echo ""
    echo "=== RESPUESTA ==="
    {
        echo "Contexto del archivo $archivo:"
        head -50 "$archivo"
        echo ""
        echo "Pregunta: $pregunta"
    } | ollama run qwen2.5-coder:1.5b 2>/dev/null
}

# f - Consultar frontend
consultar_frontend() {
    cd "$1" || return 1
    preg="$2"
    find . -type f \( -name "*.jsx" -o -name "*.tsx" -o -name "*.vue" -o -name "*.html" -o -name "*.css" \) 2>/dev/null | head -5 | while read f; do
        echo "--- $f ---"
        head -25 "$f" 2>/dev/null
    done | ollama run qwen2.5-coder:1.5b "Contexto frontend del proyecto. Pregunta: $preg"
}

# b - Consultar backend
consultar_backend() {
    cd "$1" || return 1
    preg="$2"
    find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.go" -o -name "*.sql" \) 2>/dev/null | head -5 | while read f; do
        echo "--- $f ---"
        head -25 "$f" 2>/dev/null
    done | ollama run qwen2.5-coder:1.5b "Contexto backend del proyecto. Pregunta: $preg"
}

# m - Ver mapa
m() {
    if [ -f .ia_mapa/mapa_completo.json ]; then
        jq -r '.archivos[] | "📄 \(.ruta) (\(.lineas) líneas)"' .ia_mapa/mapa_completo.json 2>/dev/null
    else
        echo "Sin mapa. Ejecuta: crear_mapa_proyecto"
    fi
}

# tech - Analizar tecnologías
tech() {
    if [ -z "$1" ]; then
        detectar_tecnologias "$PWD"
    else
        if [ -d "$PROYECTOS_DIR/$1" ]; then
            detectar_tecnologias "$PROYECTOS_DIR/$1"
        elif [ -d "$GITHUB_DIR/$1" ]; then
            detectar_tecnologias "$GITHUB_DIR/$1"
        else
            echo "❌ Proyecto '$1' no encontrado"
            return 1
        fi
    fi
}


# ============================================
# MENÚ INTERACTIVO
# ============================================

ia() {
    echo ""
    echo "=========================================="
    echo "🤖 ASISTENTE IA - MENÚ INTERACTIVO"
    echo "=========================================="
    echo ""
    echo "📁 Proyecto actual: $(basename "$PWD")"
    echo ""
    echo "1. Preguntar sobre el proyecto (q)"
    echo "2. Ver mapa de archivos (m)"
    echo "3. Preguntar sobre un archivo específico (qc)"
    echo "4. Analizar frontend (f)"
    echo "5. Analizar backend (b)"
    echo "6. Generar código con agente"
    echo "7. Analizar tecnologías (tech)"
    echo "8. Salir"
    echo ""
    read -p "Elige una opción (1-8): " opcion

    case $opcion in
        1)
            read -p "Pregunta: " pregunta
            q "$pregunta"
            ;;
        2)
            m
            ;;
        3)
            read -p "Archivo: " archivo
            read -p "Pregunta sobre $archivo: " pregunta
            qc "$archivo" "$pregunta"
            ;;
        4)
            read -p "Pregunta sobre frontend: " pregunta
            consultar_frontend "$PWD" "$pregunta"
            ;;
        5)
            read -p "Pregunta sobre backend: " pregunta
            consultar_backend "$PWD" "$pregunta"
            ;;
        6)
            echo "Agentes: a) Analista b) Backend c) Frontend d) Datos e) QA f) DevOps g) Sistema"
            read -p "Elige (a-g): " agente
            case $agente in
                a) analista ;;
                b) backend ;;
                c) frontend ;;
                d) datos ;;
                e) qa ;;
                f) devops ;;
                g) sistema ;;
                *) echo "❌ Opción inválida" ;;
            esac
            ;;
        7)
            tech "$PWD"
            ;;
        8)
            echo "👋 Hasta luego!"
            return 0
            ;;
        *)
            echo "❌ Opción inválida"
            ;;
    esac
    echo ""
    read -p "Presiona Enter para continuar..."
    ia
}


# ============================================
# ALIAS Y ATAJOS
# ============================================

# Navegación
alias ag='cd $AGENTE_HOME'
alias agp='cd $PROYECTOS_DIR'
alias agg='cd $GITHUB_DIR'
alias fin='ir FinanciusCopy'

# Proyectos
alias p='listar_proyectos'

# IA
alias f='consultar_frontend "$PWD"'
alias b='consultar_backend "$PWD"'
alias c='commit'

# Agentes del orquestador
alias analista='cd $AGENTE_HOME && python3 agente_analista.py'
alias datos='cd $AGENTE_HOME && python3 agente_datos.py'
alias backend='cd $AGENTE_HOME && python3 agente_backend.py'
alias frontend='cd $AGENTE_HOME && python3 agente_frontend.py'
alias qa='cd $AGENTE_HOME && python3 agente_qa.py'
alias devops='cd $AGENTE_HOME && python3 agente_devops.py'
alias pm='cd $AGENTE_HOME && python3 agente_pm.py'
alias sistema='cd $AGENTE_HOME && python3 agente_pm.py'


# ============================================
# MENSAJE DE BIENVENIDA
# ============================================

echo ""
echo "=========================================="
echo "✅ SISTEMA IA + AGENTES CARGADO"
echo "=========================================="
echo ""
echo "📌 PROYECTOS:"
echo "   p                  - Listar proyectos"
echo "   ir <nombre>        - Ir a proyecto"
echo "   np <nombre>        - Nuevo proyecto"
echo "   clonar <url>       - Clonar de GitHub"
echo "   fin                - Ir a FinanciusCopy"
echo ""
echo "📌 NAVEGACIÓN:"
echo "   ag | agp | agg     - Ir a agente_sistema / proyectos / github"
echo ""
echo "📌 IA ASISTENTE:"
echo "   q 'pregunta'       - Preguntar con contexto"
echo "   qc <archivo> 'p'   - Preguntar sobre archivo"
echo "   f 'pregunta'       - Solo frontend"
echo "   b 'pregunta'       - Solo backend"
echo "   m                  - Mapa de archivos"
echo "   tech [nombre]      - Detectar tecnologías"
echo "   ia                 - Menú interactivo"
echo ""
echo "📌 GIT:"
echo "   actualizar         - git pull + actualizar mapa"
echo "   commit 'mensaje'   - Commit rápido"
echo "   c 'mensaje'        - Alias de commit"
echo ""
echo "📌 AGENTES:"
echo "   analista | datos | backend | frontend | qa | devops"
echo "   sistema  (o pm)    - Ejecutar todos los agentes"
echo "=========================================="