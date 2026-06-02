#!/bin/bash
# Script para instalar y ejecutar la plataforma en macOS/Linux

echo ""
echo "===================================="
echo "EventosPlatforma - Setup para Unix"
echo "===================================="
echo ""

# Verificar si Python está instalado
if ! command -v py &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Instálalo con: brew install py"
    exit 1
fi

echo "[✓] Python detectado"

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "[*] Creando entorno virtual..."
    py -m venv venv
    echo "[✓] Entorno virtual creado"
else
    echo "[✓] Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "[*] Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "[*] Instalando dependencias..."
pip install -r requirements.txt
echo "[✓] Dependencias instaladas"

echo ""
echo "===================================="
echo "Iniciando EventosPlatforma..."
echo "===================================="
echo ""
echo "Abre tu navegador en: http://localhost:5000/"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""

# Ejecutar la aplicación
python app.py
