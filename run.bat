@echo off
REM Script para instalar y ejecutar la plataforma en Windows

echo.
echo ====================================
echo EventosPlatforma - Setup para Windows
echo ====================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [✓] Python detectado

REM Crear entorno virtual
if not exist venv (
    echo [*] Creando entorno virtual...
    python -m venv venv
    echo [✓] Entorno virtual creado
) else (
    echo [✓] Entorno virtual ya existe
)

REM Activar entorno virtual
echo [*] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [*] Instalando dependencias...
pip install -r requirements.txt
echo [✓] Dependencias instaladas

echo.
echo ====================================
echo Iniciando EventosPlatforma...
echo ====================================
echo.
echo Abre tu navegador en: http://localhost:5000/
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

REM Ejecutar la aplicación
python app.py

pause
