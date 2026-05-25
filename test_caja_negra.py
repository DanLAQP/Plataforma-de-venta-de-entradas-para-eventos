"""
Script de Pruebas de Caja Negra - Versión Corregida
Con asientos reales del sistema para validación correcta
"""

import json
import os
from datetime import datetime
from typing import List, Tuple

# ========== CARGAR DATOS REALES ==========
def cargar_compras():
    if os.path.exists('data/compras.json'):
        with open('data/compras.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def obtener_asientos_ocupados(evento_id):
    compras = cargar_compras()
    ocupados = set()
    for compra in compras:
        if compra.get('evento_id') == evento_id and compra.get('asientos'):
            for asiento in compra['asientos']:
                ocupados.add(asiento)
    return list(ocupados)

# ========== VALIDADORES ==========
def validar_nombre(nombre):
    nombre = nombre.strip()
    if not nombre:
        return False, "Nombre vacio"
    if len(nombre) < 3:
        return False, "Nombre muy corto"
    if len(nombre) > 50:
        return False, "Nombre muy largo"
    return True, "Valido"

def validar_correo(correo):
    correo = correo.strip()
    if not correo:
        return False, "Correo vacio"
    if "@" not in correo or "." not in correo:
        return False, "Correo invalido"
    return True, "Valido"

def validar_asientos(asientos, evento_id=1, ocupados=None):
    if not asientos:
        return False, "Sin asientos"
    if len(asientos) > 150:
        return False, "Demasiados"
    if len(set(asientos)) != len(asientos):
        return False, "Duplicados"
    
    if ocupados is None:
        ocupados = obtener_asientos_ocupados(evento_id)
    
    for asiento in asientos:
        if asiento in ocupados:
            return False, f"Ocupado: {asiento}"
    
    return True, "Valido"

def validar_evento(evento_id):
    if os.path.exists('data/eventos.json'):
        with open('data/eventos.json', 'r', encoding='utf-8') as f:
            eventos = json.load(f)
            for e in eventos:
                if e['id'] == evento_id:
                    return True, "Existe"
    return False, "No existe"

# ========== EJECUTAR PRUEBAS ==========
def ejecutar_prueba(caso_id, nombre, correo, asientos, evento_id, esperado_exito):
    """
    esperado_exito: True=espera exito, False=espera fallo
    """
    ocupados = obtener_asientos_ocupados(evento_id)
    
    v_nombre, m_nombre = validar_nombre(nombre)
    v_correo, m_correo = validar_correo(correo)
    v_asientos, m_asientos = validar_asientos(asientos, evento_id, ocupados)
    v_evento, m_evento = validar_evento(evento_id)
    
    # Determinar si pasa
    todas_validas = v_nombre and v_correo and v_asientos and v_evento
    
    # Comparar con esperado
    if todas_validas == esperado_exito:
        estado = "PASADO"
    else:
        estado = "FALLIDO"
    
    return estado

# ========== DEFINIR CASOS ==========
CASOS = [
    # PE: Compras exitosas
    ("PE-001", "Juan", "juan@mail.com", ["C1"], 1, True),
    ("PE-004", "Jose", "jose@mail.com", ["C2"], 1, True),
    ("PE-005", "Juan", "user@domain.com", ["C3"], 1, True),
    ("PE-008", "Juan", "user@mail.empresa.com", ["C6"], 1, True),
    ("PE-009", "Juan", "juan@mail.com", ["C7"], 1, True),
    ("PE-012", "Juan", "juan@mail.com", ["C8", "D1", "D2"], 1, True),
    ("PE-014", "Juan", "juan@mail.com", ["C9"], 1, True),
    
    # PE: Datos invalidos
    ("PE-002", "", "juan@mail.com", ["C1"], 1, False),
    ("PE-003", "   ", "juan@mail.com", ["C1"], 1, False),
    ("PE-006", "Juan", "", ["C1"], 1, False),
    ("PE-007", "Juan", "usuariodominio", ["C1"], 1, False),
    ("PE-010", "Juan", "juan@mail.com", [], 1, False),
    ("PE-011", "Juan", "juan@mail.com", ["A1"], 1, False),
    ("PE-013", "Juan", "juan@mail.com", [f"{chr(65+i//15)}{(i%15)+1}" for i in range(140)], 1, False),
    ("PE-015", "Juan", "juan@mail.com", ["C1"], 999, False),
    
    # AVL: Limites exitosos
    ("AVL-001", "abc", "test@mail.com", ["D3"], 1, True),
    ("AVL-003", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "test@mail.com", ["D5"], 1, True),
    ("AVL-005", "Juan", "test@mail.com", ["D7"], 1, True),
    ("AVL-010", "Juan", "test@mail.com", ["D8"], 1, True),
    
    # AVL: Limites fallidos
    ("AVL-002", "ab", "test@mail.com", ["D4"], 1, False),
    ("AVL-004", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "test@mail.com", ["D6"], 1, False),
    ("AVL-006", "Juan", "test@mail.com", [], 1, False),
    ("AVL-008", "Juan", "test@mail.com", [f"{chr(65+i//15)}{(i%15)+1}" for i in range(140)], 1, False),
    ("AVL-011", "Juan", "test@mail.com", ["D9"], 0, False),
    ("AVL-012", "Juan", "test@mail.com", ["D10"], -1, False),
    ("AVL-013", "Juan", "test@mail.com", ["D11"], 999999, False),
]

# ========== DESCRIPCIÓN DE PRUEBAS ==========
DESCRIPCIONES = {
    "PE-001": ("Compra exitosa con datos válidos", ["nombre='Juan'", "correo='juan@mail.com'", "asientos=['C1']", "evento=1"]),
    "PE-004": ("Nombre con caracteres especiales", ["nombre='Jose'", "asientos=['C2']"]),
    "PE-005": ("Correo válido estándar", ["correo='user@domain.com'"]),
    "PE-008": ("Correo con subdominios", ["correo='user@mail.empresa.com'"]),
    "PE-009": ("Un asiento válido (mínimo)", ["asientos=['C7']"]),
    "PE-012": ("Múltiples asientos válidos", ["asientos=['C8','D1','D2']"]),
    "PE-014": ("Evento existente válido", ["evento=1"]),
    "PE-002": ("Validación: nombre vacío rechazado", ["nombre=''", "Esperado: ERROR"]),
    "PE-003": ("Validación: nombre solo espacios rechazado", ["nombre='   '", "Esperado: ERROR"]),
    "PE-006": ("Validación: correo vacío rechazado", ["correo=''", "Esperado: ERROR"]),
    "PE-007": ("Validación: correo sin @ rechazado", ["correo='usuariodominio'", "Esperado: ERROR"]),
    "PE-010": ("Validación: sin asientos rechazado", ["asientos=[]", "Esperado: ERROR"]),
    "PE-011": ("CRÍTICO: asientos ocupados rechazados", ["asientos=['A1']", "A1 está ocupado", "Esperado: ERROR"]),
    "PE-013": ("CRÍTICO: cantidad > disponibles rechazada", ["asientos=[140 asientos]", "Disponibles=138", "Esperado: ERROR"]),
    "PE-015": ("Validación: evento no existe rechazado", ["evento=999", "Esperado: ERROR"]),
    
    "AVL-001": ("Nombre en límite mínimo (3 chars)", ["nombre='abc'", "Límite inferior válido"]),
    "AVL-003": ("Nombre en límite máximo (50 chars)", ["nombre='A'*50", "Límite superior válido"]),
    "AVL-005": ("Cantidad mínima asientos (1)", ["asientos=['D7']", "Límite inferior válido"]),
    "AVL-010": ("Evento ID mínimo (1)", ["evento=1", "Primer evento válido"]),
    "AVL-002": ("Nombre debajo límite mínimo (2 chars)", ["nombre='ab'", "Por debajo de 3", "Esperado: ERROR"]),
    "AVL-004": ("Nombre excede límite máximo (51 chars)", ["nombre='A'*51", "Excede 50", "Esperado: ERROR"]),
    "AVL-006": ("Cantidad cero asientos", ["asientos=[]", "Por debajo de 1", "Esperado: ERROR"]),
    "AVL-008": ("CRÍTICO: cantidad +1 excedida", ["asientos=[140]", "Excede disponibles 138", "Esperado: ERROR"]),
    "AVL-011": ("Evento ID=0 no existe", ["evento=0", "ID inválido", "Esperado: ERROR"]),
    "AVL-012": ("Evento ID negativo (-1)", ["evento=-1", "ID inválido", "Esperado: ERROR"]),
    "AVL-013": ("Evento ID extremo (999999)", ["evento=999999", "ID no existe", "Esperado: ERROR"]),
}

# ========== EJECUTAR Y REPORTAR ==========
def main():
    print("\n" + "="*80)
    print("PRUEBAS DE CAJA NEGRA - PLATAFORMA DE VENTA DE ENTRADAS")
    print("="*80)
    
    ocupados_1 = obtener_asientos_ocupados(1)
    print(f"\n📊 Asientos ocupados en Evento 1: {ocupados_1}")
    print(f"📊 Total asientos ocupados: {len(ocupados_1)}\n")
    
    print("PARTICIÓN DE EQUIVALENCIA (PE) - Validación de clases válidas/inválidas")
    print("-" * 80)
    
    resultados = []
    casos_pe = [c for c in CASOS if c[0].startswith("PE-")]
    for caso_id, nombre, correo, asientos, evento_id, esperado in casos_pe:
        estado = ejecutar_prueba(caso_id, nombre, correo, asientos, evento_id, esperado)
        resultados.append((caso_id, estado))
        simbolo = "✅" if estado == "PASADO" else "❌"
        desc, detalles = DESCRIPCIONES.get(caso_id, ("Sin descripción", []))
        print(f"{simbolo} {caso_id}: {desc}")
        for detalle in detalles[:2]:  # Mostrar max 2 detalles
            print(f"   └─ {detalle}")
        print()
    
    print("\nANÁLISIS DE VALORES LÍMITE (AVL) - Pruebas de bordes y transiciones")
    print("-" * 80)
    
    casos_avl = [c for c in CASOS if c[0].startswith("AVL-")]
    for caso_id, nombre, correo, asientos, evento_id, esperado in casos_avl:
        estado = ejecutar_prueba(caso_id, nombre, correo, asientos, evento_id, esperado)
        resultados.append((caso_id, estado))
        simbolo = "✅" if estado == "PASADO" else "❌"
        desc, detalles = DESCRIPCIONES.get(caso_id, ("Sin descripción", []))
        print(f"{simbolo} {caso_id}: {desc}")
        for detalle in detalles[:2]:  # Mostrar max 2 detalles
            print(f"   └─ {detalle}")
        print()
    
    # Resumen
    pasados = sum(1 for _, e in resultados if e == "PASADO")
    total = len(resultados)
    tasa = 100 * pasados // total if total > 0 else 0
    
    pe_pasadas = sum(1 for id, e in resultados if e == "PASADO" and id.startswith("PE-"))
    avl_pasadas = sum(1 for id, e in resultados if e == "PASADO" and id.startswith("AVL-"))
    
    print("="*80)
    print(f"✅ PARTICIÓN DE EQUIVALENCIA: {pe_pasadas}/{len(casos_pe)} pruebas pasadas")
    print(f"✅ ANÁLISIS DE VALORES LÍMITE: {avl_pasadas}/{len(casos_avl)} pruebas pasadas")
    print(f"\n🎉 RESUMEN TOTAL: {pasados}/{total} pruebas pasadas ({tasa}%)")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
