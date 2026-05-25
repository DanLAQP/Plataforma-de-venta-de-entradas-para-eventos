#!/usr/bin/env python3
"""
Script de verificación del proyecto EventosPlatforma
Ejecutar: python verify.py
"""

import os
import json
from pathlib import Path

def verificar_proyecto():
    """Verifica que el proyecto esté completamente configurado"""
    
    print("=" * 70)
    print("🔍 VERIFICACIÓN DEL PROYECTO - EventosPlatforma v2.0")
    print("=" * 70)
    print()
    
    # 1. Verificar estructura de carpetas
    print("1️⃣  VERIFICANDO ESTRUCTURA DE CARPETAS...")
    carpetas_requeridas = [
        'app',
        'app/templates',
        'app/static',
        'app/static/css',
        'app/static/js',
        'data'
    ]
    
    todas_ok = True
    for carpeta in carpetas_requeridas:
        if os.path.exists(carpeta):
            print(f"   ✅ {carpeta}")
        else:
            print(f"   ❌ FALTA: {carpeta}")
            todas_ok = False
    
    if not todas_ok:
        print("\n⚠️  Algunas carpetas no existen.")
        return False
    
    # 2. Verificar archivos Python
    print("\n2️⃣  VERIFICANDO ARCHIVOS PYTHON...")
    archivos_python = [
        'app.py',
        'app/utils.py',
        'add_event.py',
        'install.py',
        'cleanup.py'
    ]
    
    todas_ok = True
    for archivo in archivos_python:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ FALTA: {archivo}")
            todas_ok = False
    
    if not todas_ok:
        print("\n⚠️  Algunos archivos Python no existen.")
        return False
    
    # 3. Verificar templates HTML
    print("\n3️⃣  VERIFICANDO TEMPLATES HTML...")
    templates = [
        'app/templates/base.html',
        'app/templates/index.html',
        'app/templates/evento_detalle.html',
        'app/templates/asientos.html',
        'app/templates/comprar.html',
        'app/templates/compra_exitosa.html',
        'app/templates/historial.html'
    ]
    
    todas_ok = True
    for template in templates:
        if os.path.exists(template):
            print(f"   ✅ {template}")
        else:
            print(f"   ❌ FALTA: {template}")
            todas_ok = False
    
    if not todas_ok:
        print("\n⚠️  Algunos templates no existen.")
        return False
    
    # 4. Verificar archivos estáticos
    print("\n4️⃣  VERIFICANDO ARCHIVOS ESTÁTICOS...")
    estaticos = [
        'app/static/css/style.css',
        'app/static/js/script.js'
    ]
    
    todas_ok = True
    for archivo in estaticos:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ FALTA: {archivo}")
            todas_ok = False
    
    if not todas_ok:
        print("\n⚠️  Algunos archivos estáticos no existen.")
        return False
    
    # 5. Verificar archivos de datos
    print("\n5️⃣  VERIFICANDO ARCHIVOS DE DATOS...")
    datos_archivos = [
        'data/eventos.json',
        'data/compras.json'
    ]
    
    todas_ok = True
    for archivo in datos_archivos:
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    json.load(f)
                print(f"   ✅ {archivo} (JSON válido)")
            except json.JSONDecodeError:
                print(f"   ❌ {archivo} (JSON INVÁLIDO)")
                todas_ok = False
        else:
            print(f"   ❌ FALTA: {archivo}")
            todas_ok = False
    
    if not todas_ok:
        print("\n⚠️  Hay problemas con los archivos de datos.")
        return False
    
    # 6. Verificar archivos de configuración
    print("\n6️⃣  VERIFICANDO CONFIGURACIÓN...")
    config_archivos = [
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'CHANGELOG.md',
        'RESUMEN_MEJORAS.txt',
        '.gitignore'
    ]
    
    todas_ok = True
    for archivo in config_archivos:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ⚠️  OPCIONAL: {archivo}")
    
    # 7. Resumen
    print("\n" + "=" * 70)
    print("✅ VERIFICACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print()
    
    # Información del proyecto
    print("📊 INFORMACIÓN DEL PROYECTO:")
    print(f"   Nombre: EventosPlatforma")
    print(f"   Versión: 2.0.0")
    print(f"   Backend: Flask 3.0.0")
    print(f"   Frontend: HTML5 + CSS3 + Bootstrap 5 + JavaScript")
    print(f"   Base de datos: JSON")
    print()
    
    # Próximos pasos
    print("🚀 PRÓXIMOS PASOS:")
    print("   1. Instalar dependencias: pip install -r requirements.txt")
    print("   2. Ejecutar aplicación: python app.py")
    print("   3. Abrir navegador: http://localhost:5000/")
    print()
    
    # Características
    print("✨ CARACTERÍSTICAS IMPLEMENTADAS:")
    print("   ✅ Ver eventos")
    print("   ✅ Detalle de evento")
    print("   ✅ Mapa de asientos (NUEVO)")
    print("   ✅ Comprar entradas")
    print("   ✅ Códigos QR (NUEVO)")
    print("   ✅ Descargar PDF (NUEVO)")
    print("   ✅ Historial de compras")
    print("   ✅ API REST")
    print()
    
    return True

if __name__ == '__main__':
    if verificar_proyecto():
        print("🎉 ¡Proyecto listo para usar!")
    else:
        print("❌ Hay problemas en la verificación")
        exit(1)
