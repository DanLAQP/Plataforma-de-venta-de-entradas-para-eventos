"""
Script para agregar eventos a la plataforma
Uso: python add_event.py
"""

import json
import os

EVENTOS_FILE = 'data/eventos.json'

def cargar_eventos():
    """Carga eventos desde el archivo JSON"""
    if os.path.exists(EVENTOS_FILE):
        with open(EVENTOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_eventos(eventos):
    """Guarda eventos en el archivo JSON"""
    with open(EVENTOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(eventos, f, indent=2, ensure_ascii=False)

def agregar_evento():
    """Agrega un nuevo evento de forma interactiva"""
    eventos = cargar_eventos()
    
    # Obtener el siguiente ID
    nuevo_id = max([e['id'] for e in eventos], default=0) + 1
    
    print("\n" + "="*50)
    print("AGREGAR NUEVO EVENTO")
    print("="*50 + "\n")
    
    nombre = input("Nombre del evento: ").strip()
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    ubicacion = input("Ubicación: ").strip()
    precio = float(input("Precio por entrada ($): ").strip())
    entradas = int(input("Cantidad de entradas disponibles: ").strip())
    imagen = input("URL de la imagen (opcional, presiona Enter para usar placeholder): ").strip()
    descripcion = input("Descripción: ").strip()
    
    if not imagen:
        imagen = f"https://via.placeholder.com/400x300?text={nombre.replace(' ', '+')}"
    
    nuevo_evento = {
        'id': nuevo_id,
        'nombre': nombre,
        'fecha': fecha,
        'ubicacion': ubicacion,
        'precio': precio,
        'entradas_disponibles': entradas,
        'imagen': imagen,
        'descripcion': descripcion
    }
    
    eventos.append(nuevo_evento)
    guardar_eventos(eventos)
    
    print(f"\n✓ Evento creado exitosamente con ID: {nuevo_id}")
    print(f"  Nombre: {nombre}")
    print(f"  Fecha: {fecha}")
    print(f"  Precio: ${precio:.2f}\n")

def listar_eventos():
    """Lista todos los eventos"""
    eventos = cargar_eventos()
    
    if not eventos:
        print("\nNo hay eventos registrados.\n")
        return
    
    print("\n" + "="*80)
    print("EVENTOS DISPONIBLES")
    print("="*80 + "\n")
    
    for evento in eventos:
        print(f"ID: {evento['id']}")
        print(f"  Nombre: {evento['nombre']}")
        print(f"  Fecha: {evento['fecha']}")
        print(f"  Ubicación: {evento['ubicacion']}")
        print(f"  Precio: ${evento['precio']:.2f}")
        print(f"  Entradas disponibles: {evento['entradas_disponibles']}")
        print(f"  Descripción: {evento['descripcion'][:50]}...")
        print()

def menu():
    """Menú principal"""
    while True:
        print("\n" + "="*50)
        print("GESTOR DE EVENTOS")
        print("="*50)
        print("\n1. Agregar nuevo evento")
        print("2. Listar eventos")
        print("3. Salir")
        
        opcion = input("\nSelecciona una opción (1-3): ").strip()
        
        if opcion == '1':
            agregar_evento()
        elif opcion == '2':
            listar_eventos()
        elif opcion == '3':
            print("\n¡Hasta luego!\n")
            break
        else:
            print("\nOpción inválida. Intenta de nuevo.")

if __name__ == '__main__':
    menu()
