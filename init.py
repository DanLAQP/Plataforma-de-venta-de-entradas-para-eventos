#!/usr/bin/env python3
"""
Script de inicialización completa del proyecto
Instala dependencias, crea estructura y resetea datos
"""

import subprocess
import sys
import os

def main():
    print("\n" + "=" * 70)
    print(" 🚀 INICIALIZACIÓN DE EventosPlatforma v2.0")
    print("=" * 70 + "\n")
    
    # 1. Instalar dependencias
    print("📦 Paso 1: Instalando dependencias...")
    print("-" * 70)
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
            capture_output=True,
            timeout=60
        )
        
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            capture_output=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("✅ Dependencias instaladas correctamente\n")
        else:
            print(f"⚠️  Advertencia: {result.stderr.decode()}\n")
            
    except subprocess.TimeoutExpired:
        print("⏱️  Timeout durante la instalación. Intenta manualmente:")
        print("   python -m pip install -r requirements.txt\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False
    
    # 2. Crear estructura de directorios
    print("📂 Paso 2: Creando estructura de directorios...")
    print("-" * 70)
    
    dirs = ['data', 'app/templates', 'app/static/css', 'app/static/js', 'app/temp']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✅ Estructura de directorios lista\n")
    
    # 3. Resetear datos
    print("🔄 Paso 3: Reseteando datos iniciales...")
    print("-" * 70)
    try:
        from reset_data import crear_datos_iniciales
        if crear_datos_iniciales():
            print("✅ Datos inicializados\n")
        else:
            print("❌ Error al inicializar datos\n")
            return False
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False
    
    # 4. Verificar instalación
    print("🔍 Paso 4: Verificando instalación...")
    print("-" * 70)
    
    required_packages = ['flask', 'qrcode', 'PIL', 'reportlab']
    all_ok = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} no instalado")
            all_ok = False
    
    print()
    
    if not all_ok:
        print("⚠️  Algunas dependencias no están instaladas.")
        print("   Ejecuta: python -m pip install -r requirements.txt\n")
        return False
    
    # 5. Resumen final
    print("=" * 70)
    print(" ✅ INICIALIZACIÓN COMPLETADA CON ÉXITO")
    print("=" * 70)
    print()
    print("🎯 PRÓXIMO PASO: Ejecuta la aplicación")
    print()
    print("   $ python app.py")
    print()
    print("   Luego abre en tu navegador:")
    print("   👉 http://localhost:5000/")
    print()
    print("=" * 70 + "\n")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
