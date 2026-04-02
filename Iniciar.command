#!/bin/bash
# Estatística Policial - Duplo clique para abrir no Mac

cd "$(dirname "$0")"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    osascript -e 'display alert "Python 3 não encontrado" message "Instale em: https://www.python.org/downloads/" as critical'
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    osascript -e 'display alert "Node.js não encontrado" message "Instale em: https://nodejs.org/" as critical'
    exit 1
fi

python3 launcher.py
