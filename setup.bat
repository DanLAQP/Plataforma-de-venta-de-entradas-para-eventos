@echo off
REM Script de inicio para EventosPlatforma (Windows)
REM Uso: setup.bat

echo.
echo ================================================================
echo  EventosPlatforma v2.1 - SETUP AUTOMATICO
echo ================================================================
echo.

REM Instalar dependencias
echo Instalando dependencias...
pip install --upgrade pip > nul 2>&1
pip install -r requirements.txt > nul 2>&1

if %ERRORLEVEL% NEQ 0 (
    echo Error durante instalacion. Intenta:
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

echo OK
echo.

REM Crear estructura
echo Creando estructura...
if not exist "data" mkdir data
if not exist "app\templates" mkdir app\templates
if not exist "app\static\css" mkdir app\static\css
if not exist "app\static\js" mkdir app\static\js
if not exist "app\temp" mkdir app\temp
echo OK
echo.

REM Resetear datos
echo Reseteando datos iniciales...
python reset_data.py > nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo OK
) else (
    echo Advertencia: No se pudieron resetear datos
)

echo.
echo ================================================================
echo  LISTO PARA EJECUTAR
echo ================================================================
echo.
echo Proximos pasos:
echo   1. Ejecuta: python app.py
echo   2. Abre: http://localhost:5000/
echo.
pause
