#!/usr/bin/env python3
"""
Script para resetear datos iniciales
Crear estructura JSON correcta para eventos y compras
"""

import json
import os

def crear_datos_iniciales():
    """Crea datos iniciales para la aplicación"""
    
    print("=" * 60)
    print("Reseteando datos iniciales...")
    print("=" * 60)
    print()
    
    # Crear directorio data si no existe
    os.makedirs('data', exist_ok=True)
    
    # Datos de eventos iniciales
    eventos = [
        {
            "id": 1,
            "nombre": "Festival de Música 2026",
            "fecha": "2026-06-15",
            "ubicacion": "Estadio Nacional",
            "precio": 45.0,
            "entradas_disponibles": 495,
            "imagen": "https://gladyspalmera.com/wp-content/uploads/2021/11/festival.jpg",
            "descripcion": "Gran festival de música en vivo con los mejores artistas del momento."
        },
        {
            "id": 2,
            "nombre": "Conferencia de Tecnología",
            "fecha": "2026-07-20",
            "ubicacion": "Centro de Convenciones",
            "precio": 25.0,
            "entradas_disponibles": 200,
            "imagen": "https://www.cuc.edu.co/wp-content/uploads/2022/07/DSC00353-1-1.jpg",
            "descripcion": "Únete a expertos en tecnología para aprender sobre las últimas tendencias."
        },
        {
            "id": 3,
            "nombre": "Concierto de Rock",
            "fecha": "2026-08-10",
            "ubicacion": "Anfiteatro Municipal",
            "precio": 55.0,
            "entradas_disponibles": 300,
            "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNwsHNSWIKhUu27ZBNtgVyoETnRJgX2XTgxg&s",
            "descripcion": "Vive la energía del rock en vivo con bandas nacionales e internacionales."
        },
        {
            "id": 4,
            "nombre": "Expo de Arte Contemporáneo",
            "fecha": "2026-09-05",
            "ubicacion": "Museo de Arte Moderno",
            "precio": 15.0,
            "entradas_disponibles": 149,
            "imagen": "https://thebestofdr.do/wp-content/uploads/2024/06/0a29d0ef57ced3a7c1d1ed4eda5e2ff6_XL.jpeg",
            "descripcion": "Explora las obras maestras del arte contemporáneo."
        }
    ]
    
    # Datos de compras iniciales (ejemplo con asientos reales)
    compras = [
        {
            "id": 1,
            "evento_id": 1,
            "evento_nombre": "Festival de Música 2026",
            "nombre": "Luis Daniel",
            "correo": "laguero@unsa.edu.pe",
            "cantidad": 2,
            "precio_unitario": 45.0,
            "total": 90.0,
            "fecha_compra": "2026-05-24 22:08:38",
            "codigo_qr": "ENTRADA-1-1",
            "asientos": ["A1", "A2"]
        },
        {
            "id": 2,
            "evento_id": 4,
            "evento_nombre": "Expo de Arte Contemporáneo",
            "nombre": "Luis Daniel",
            "correo": "laguero@unsa.edu.pe",
            "cantidad": 1,
            "precio_unitario": 15.0,
            "total": 15.0,
            "fecha_compra": "2026-05-24 22:32:55",
            "codigo_qr": "ENTRADA-2-4",
            "asientos": ["A1"]
        },
        {
            "id": 3,
            "evento_id": 1,
            "evento_nombre": "Festival de Música 2026",
            "nombre": "Juan Pérez",
            "correo": "juan@example.com",
            "cantidad": 1,
            "precio_unitario": 45.0,
            "total": 45.0,
            "fecha_compra": "2026-05-24 22:37:09",
            "codigo_qr": "ENTRADA-3-1",
            "asientos": ["B1"]
        }
    ]
    
    # Guardar eventos.json
    try:
        with open('data/eventos.json', 'w', encoding='utf-8') as f:
            json.dump(eventos, f, indent=2, ensure_ascii=False)
        print("✅ eventos.json creado correctamente")
    except Exception as e:
        print(f"❌ Error al guardar eventos.json: {e}")
        return False
    
    # Guardar compras.json
    try:
        with open('data/compras.json', 'w', encoding='utf-8') as f:
            json.dump(compras, f, indent=2, ensure_ascii=False)
        print("✅ compras.json creado correctamente")
    except Exception as e:
        print(f"❌ Error al guardar compras.json: {e}")
        return False
    
    print()
    print("=" * 60)
    print("✅ Datos iniciales creados correctamente")
    print("=" * 60)
    print()
    print("Resumen:")
    print(f"  • {len(eventos)} eventos creados")
    print(f"  • {len(compras)} compras de ejemplo")
    print(f"  • Asientos ocupados en evento 1: A1, A2, B1")
    print(f"  • Asientos ocupados en evento 4: A1")
    print()
    
    return True

if __name__ == '__main__':
    crear_datos_iniciales()
