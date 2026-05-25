"""
Script para limpiar archivos temporales
Uso: python cleanup.py
"""

import os
import shutil
from pathlib import Path

def limpiar_temporales():
    """Elimina archivos temporales"""
    print("🧹 Limpiando archivos temporales...\n")
    
    # Directorios a limpiar
    directorios = [
        'app/temp',
        '__pycache__',
        '.pytest_cache',
        '.vscode/__pycache__'
    ]
    
    for directorio in directorios:
        if os.path.exists(directorio):
            try:
                if os.path.isdir(directorio):
                    shutil.rmtree(directorio)
                    print(f"✅ Eliminado: {directorio}")
                else:
                    os.remove(directorio)
                    print(f"✅ Eliminado: {directorio}")
            except Exception as e:
                print(f"⚠️  No se pudo eliminar {directorio}: {e}")
    
    # Archivos a limpiar
    archivos = [
        'app/static/temp_qr_*.png'
    ]
    
    for patron in archivos:
        for archivo in Path('.').glob(patron):
            try:
                os.remove(str(archivo))
                print(f"✅ Eliminado: {archivo}")
            except Exception as e:
                print(f"⚠️  No se pudo eliminar {archivo}: {e}")
    
    print("\n✅ Limpieza completada")

def resetear_datos():
    """Resetea los datos de la aplicación (opcional)"""
    print("\n⚠️  ¿Deseas resetear todos los datos? (s/n)")
    respuesta = input("Respuesta: ").strip().lower()
    
    if respuesta == 's':
        import json
        
        # Resetear compras
        with open('data/compras.json', 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2)
        print("✅ Compras reseteadas")
        
        # Resetear eventos a valores por defecto
        eventos_default = [
            {
                "id": 1,
                "nombre": "Festival de Música 2026",
                "fecha": "2026-06-15",
                "ubicacion": "Estadio Nacional",
                "precio": 45.0,
                "entradas_disponibles": 500,
                "imagen": "https://via.placeholder.com/400x300?text=Festival+de+M%C3%BAsica",
                "descripcion": "Gran festival de música en vivo..."
            }
        ]
        
        with open('data/eventos.json', 'w', encoding='utf-8') as f:
            json.dump(eventos_default, f, indent=2, ensure_ascii=False)
        print("✅ Eventos reseteados")

if __name__ == '__main__':
    limpiar_temporales()
    
    print("\n" + "="*50)
    respuesta = input("¿Deseas resetear los datos? (s/n): ").strip().lower()
    
    if respuesta == 's':
        resetear_datos()
    
    print("\n✅ Proceso completado")
