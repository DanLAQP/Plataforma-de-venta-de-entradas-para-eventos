"""
Script de Diagnóstico - Identificar el problema exacto con validaciones
"""

import json
import os
from datetime import datetime

EVENTOS_FILE = 'data/eventos.json'
COMPRAS_FILE = 'data/compras.json'

def cargar_eventos():
    if os.path.exists(EVENTOS_FILE):
        with open(EVENTOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def cargar_compras():
    if os.path.exists(COMPRAS_FILE):
        with open(COMPRAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def obtener_asientos_ocupados(evento_id):
    """Obtiene lista de asientos ocupados para un evento desde compras.json"""
    compras = cargar_compras()
    asientos_ocupados = set()
    
    for compra in compras:
        if compra.get('evento_id') == evento_id and compra.get('asientos'):
            for asiento in compra['asientos']:
                asientos_ocupados.add(asiento)
    
    return list(asientos_ocupados)

def diagnostico():
    """Ejecuta diagnóstico"""
    print("\n" + "="*80)
    print("DIAGNÓSTICO DE VALIDACIONES")
    print("="*80)
    
    # 1. Revisar eventos
    print("\n[1] ESTADO DE EVENTOS:")
    eventos = cargar_eventos()
    for evento in eventos:
        print(f"  • Evento {evento['id']}: {evento['nombre']}")
        print(f"    Entradas disponibles: {evento.get('entradas_disponibles', 'N/A')}")
    
    # 2. Revisar compras
    print("\n[2] ESTADO DE COMPRAS:")
    compras = cargar_compras()
    if compras:
        for compra in compras:
            print(f"  • Compra {compra['id']}: {compra['nombre']}")
            print(f"    Evento: {compra.get('evento_id')}")
            print(f"    Asientos: {compra.get('asientos')}")
            print(f"    Cantidad: {compra.get('cantidad')}")
    else:
        print("  (No hay compras registradas)")
    
    # 3. Validar ocupación
    print("\n[3] VALIDACIÓN DE ASIENTOS OCUPADOS:")
    if eventos:
        evento_id = eventos[0]['id']
        asientos_ocupados = obtener_asientos_ocupados(evento_id)
        print(f"  Evento {evento_id}:")
        print(f"  Asientos ocupados: {asientos_ocupados if asientos_ocupados else '(ninguno)'}")
        
        # 4. Test de validación
        print("\n[4] TEST DE VALIDACIÓN:")
        test_asientos = ["A1", "B2", "C3"]
        print(f"  Intentando comprar: {test_asientos}")
        
        for asiento in test_asientos:
            if asiento in asientos_ocupados:
                print(f"    ❌ {asiento} - RECHAZADO (ocupado)")
            else:
                print(f"    ✅ {asiento} - ACEPTADO (disponible)")
        
        # 5. Test cantidad
        print("\n[5] TEST DE CANTIDAD:")
        evento = eventos[0]
        cantidad_seleccionada = 10
        disponibles = evento.get('entradas_disponibles', 0)
        print(f"  Seleccionados: {cantidad_seleccionada}")
        print(f"  Disponibles: {disponibles}")
        
        if cantidad_seleccionada > disponibles:
            print(f"  ❌ RECHAZADO - Supera cantidad disponible")
        else:
            print(f"  ✅ ACEPTADO - Dentro de límites")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    diagnostico()
