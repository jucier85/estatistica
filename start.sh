#!/usr/bin/env bash
# ==============================================================
# Estatística Policial - Script de Inicialização
# Instala dependências, configura API key e inicia os servidores
# ==============================================================

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
ENV_FILE="$BACKEND_DIR/.env"

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════╗"
echo "║   🛡️  Estatística Policial - Dashboard IA    ║"
echo "║   Análise de Produtividade Policial          ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${NC}"

# -----------------------------------------------
# 1. Verificar dependências do sistema
# -----------------------------------------------
echo -e "${YELLOW}[1/5] Verificando dependências do sistema...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Erro: python3 não encontrado. Instale Python 3.10+.${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}Erro: node não encontrado. Instale Node.js 18+.${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}Erro: npm não encontrado. Instale Node.js 18+.${NC}"
    exit 1
fi

echo -e "  Python: $(python3 --version)"
echo -e "  Node:   $(node --version)"
echo -e "  npm:    $(npm --version)"
echo -e "${GREEN}  OK${NC}"

# -----------------------------------------------
# 2. Configurar API Key do Gemini (primeira vez)
# -----------------------------------------------
echo ""
echo -e "${YELLOW}[2/5] Configurando API Key...${NC}"

setup_api_key() {
    echo ""
    echo -e "${BLUE}Para usar a análise com IA, você precisa de uma API Key do Google Gemini.${NC}"
    echo -e "${BLUE}Obtenha gratuitamente em: https://aistudio.google.com/apikey${NC}"
    echo ""
    read -rp "Cole sua GEMINI_API_KEY: " API_KEY

    if [ -z "$API_KEY" ]; then
        echo -e "${RED}API Key vazia. A análise com IA não funcionará.${NC}"
        echo -e "${YELLOW}Você pode configurar depois editando: $ENV_FILE${NC}"
        API_KEY="your_gemini_api_key_here"
    fi

    cat > "$ENV_FILE" <<EOL
GEMINI_API_KEY=$API_KEY
ALLOWED_ORIGINS=http://localhost:5173
MAX_UPLOAD_SIZE_MB=50
EOL

    echo -e "${GREEN}  API Key salva em $ENV_FILE${NC}"
}

if [ ! -f "$ENV_FILE" ]; then
    setup_api_key
else
    # Verifica se a key ainda é o placeholder
    CURRENT_KEY=$(grep "^GEMINI_API_KEY=" "$ENV_FILE" | cut -d'=' -f2)
    if [ "$CURRENT_KEY" = "your_gemini_api_key_here" ] || [ -z "$CURRENT_KEY" ]; then
        echo -e "${YELLOW}  API Key não configurada.${NC}"
        setup_api_key
    else
        echo -e "${GREEN}  API Key já configurada.${NC}"
        read -rp "  Deseja alterar a API Key? (s/N): " CHANGE_KEY
        if [ "$CHANGE_KEY" = "s" ] || [ "$CHANGE_KEY" = "S" ]; then
            setup_api_key
        fi
    fi
fi

# -----------------------------------------------
# 3. Instalar dependências do Backend
# -----------------------------------------------
echo ""
echo -e "${YELLOW}[3/5] Instalando dependências do backend...${NC}"

if [ ! -d "$BACKEND_DIR/.venv" ]; then
    python3 -m venv "$BACKEND_DIR/.venv"
    echo -e "  Ambiente virtual criado."
fi

source "$BACKEND_DIR/.venv/bin/activate"
pip install -q -r "$BACKEND_DIR/requirements.txt" 2>&1 | tail -1
echo -e "${GREEN}  Backend OK${NC}"

# -----------------------------------------------
# 4. Instalar dependências do Frontend
# -----------------------------------------------
echo ""
echo -e "${YELLOW}[4/5] Instalando dependências do frontend...${NC}"

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    cd "$FRONTEND_DIR"
    npm install --silent 2>&1 | tail -1
    cd "$ROOT_DIR"
fi
echo -e "${GREEN}  Frontend OK${NC}"

# -----------------------------------------------
# 5. Iniciar servidores
# -----------------------------------------------
echo ""
echo -e "${YELLOW}[5/5] Iniciando servidores...${NC}"

cleanup() {
    echo ""
    echo -e "${YELLOW}Encerrando servidores...${NC}"
    kill "$BACKEND_PID" 2>/dev/null
    kill "$FRONTEND_PID" 2>/dev/null
    echo -e "${GREEN}Encerrado.${NC}"
    exit 0
}
trap cleanup SIGINT SIGTERM

# Backend
cd "$BACKEND_DIR"
source .venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd "$ROOT_DIR"

# Frontend
cd "$FRONTEND_DIR"
npm run dev -- --port 5173 &
FRONTEND_PID=$!
cd "$ROOT_DIR"

sleep 3

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Servidores iniciados com sucesso!          ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║   Frontend: http://localhost:5173             ║${NC}"
echo -e "${GREEN}║   Backend:  http://localhost:8000             ║${NC}"
echo -e "${GREEN}║   API Docs: http://localhost:8000/docs        ║${NC}"
echo -e "${GREEN}║                                              ║${NC}"
echo -e "${GREEN}║   Pressione Ctrl+C para encerrar             ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
echo ""

wait
