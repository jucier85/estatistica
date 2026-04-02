@echo off
title Estatistica Policial - Dashboard IA
echo.
echo  ========================================
echo    Estatistica Policial - Dashboard IA
echo  ========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Baixe e instale o Python em: https://www.python.org/downloads/
    echo IMPORTANTE: Marque "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)

:: Verificar Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Node.js nao encontrado!
    echo.
    echo Baixe e instale o Node.js em: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo Iniciando aplicativo...
echo.
python "%~dp0launcher.py"
pause
