#!/usr/bin/env bash
# Script rápido de inicio para macOS/Linux
# Uso: bash quick-start.sh

echo "🚀 Iniciando EventosPlatforma..."
echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt > /dev/null 2>&1

# Iniciar aplicación
echo ""
echo "============================================"
echo "✅ EventosPlatforma está iniciando..."
echo "============================================"
echo ""
echo "🌐 Abre tu navegador en:"
echo "   http://localhost:5000/"
echo ""
echo "⚠️  Presiona Ctrl+C para detener"
echo ""

python app.py
