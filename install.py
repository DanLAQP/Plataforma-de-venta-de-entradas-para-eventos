"""
Script de instalación y verificación de dependencias
Ejecutar: python install.py
"""

import subprocess
import sys
import os

def instalar_dependencias():
    """Instala las dependencias necesarias"""
    print("=" * 60)
    print("EventosPlatforma - Instalación de Dependencias")
    print("=" * 60)
    print()
    
    # Verificar que requirements.txt existe
    if not os.path.exists('requirements.txt'):
        print("❌ Error: No se encontró requirements.txt")
        return False
    
    print("📦 Instalando dependencias...")
    print()
    
    try:
        # Instalar dependencias
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        
        print()
        print("✅ Dependencias instaladas correctamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print()
        print(f"❌ Error durante la instalación: {e}")
        return False

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    print()
    print("Verificando dependencias...")
    print()
    
    dependencias = {
        'flask': 'Flask',
        'qrcode': 'QRCode',
        'PIL': 'Pillow',
        'reportlab': 'ReportLab'
    }
    
    todas_ok = True
    
    for modulo, nombre in dependencias.items():
        try:
            __import__(modulo)
            print(f"✅ {nombre} - Instalado")
        except ImportError:
            print(f"❌ {nombre} - NO instalado")
            todas_ok = False
    
    return todas_ok

def crear_directorios():
    """Crea directorios necesarios"""
    print()
    print("Creando directorios...")
    print()
    
    directorios = [
        'data',
        'app/templates',
        'app/static/css',
        'app/static/js',
        'app/temp'
    ]
    
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"✅ Creado: {directorio}")
        else:
            print(f"ℹ️  Existe: {directorio}")

def verificar_archivos():
    """Verifica que existan los archivos necesarios"""
    print()
    print("Verificando archivos...")
    print()
    
    archivos = [
        'app.py',
        'app/utils.py',
        'requirements.txt',
        'data/eventos.json',
        'data/compras.json'
    ]
    
    todas_ok = True
    
    for archivo in archivos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - FALTA")
            todas_ok = False
    
    return todas_ok

def main():
    """Función principal"""
    
    # Crear directorios
    crear_directorios()
    
    # Instalar dependencias
    if not instalar_dependencias():
        print()
        print("No se pudieron instalar todas las dependencias.")
        sys.exit(1)
    
    # Verificar dependencias
    if not verificar_dependencias():
        print()
        print("⚠️  Algunas dependencias no están instaladas.")
        print("Intenta ejecutar: pip install -r requirements.txt")
        sys.exit(1)
    
    # Verificar archivos
    print()
    if not verificar_archivos():
        print()
        print("⚠️  Faltan algunos archivos del proyecto.")
        sys.exit(1)
    
    # Éxito
    print()
    print("=" * 60)
    print("✅ ¡Instalación completada correctamente!")
    print("=" * 60)
    print()
    print("Próximo paso: Ejecuta 'python app.py'")
    print()
    print("Abre tu navegador en: http://localhost:5000/")
    print()

if __name__ == '__main__':
    main()
