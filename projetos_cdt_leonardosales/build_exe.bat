@echo off
title Compilador de Executavel - Monitor de Produtos
echo ===============================================
echo   Gerando o executavel MonitorProdutos.exe
echo ===============================================

echo.
echo 1. Instalando e atualizando dependencias...
python -m pip install --upgrade pip
python -m pip install pyinstaller selenium pandas openpyxl ttkbootstrap

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao instalar as dependencias. 
    echo Verifique se o Python e o pip estao instalados e adicionados ao PATH do Windows.
    pause
    exit /b 1
)

echo.
echo 2. Criando o executavel (.exe)...
REM Usamos "python -m PyInstaller" para garantir que utilize o executavel Python ativo.
REM --onefile: Empacota tudo em um unico arquivo .exe
REM --windowed: Oculta a tela preta de terminal (prompt de comando) ao abrir o programa.
REM --collect-all: Garante que temas do ttkbootstrap e dependencias do selenium/pandas sejam embutidos.

python -m PyInstaller --onefile --windowed --collect-all selenium --collect-all ttkbootstrap --collect-all pandas --name MonitorProdutos app_MonitorProdutos-version1.py

if errorlevel 1 (
    echo.
    echo [ERRO] Falha na geracao do executavel. Verifique as mensagens acima.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo  SUCESSO! O executavel foi criado com sucesso!
echo  O seu programa esta localizado em: dist\MonitorProdutos.exe
echo ===============================================
pause