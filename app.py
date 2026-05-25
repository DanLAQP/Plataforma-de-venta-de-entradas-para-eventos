from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
import json
import os
from datetime import datetime
from app.utils import generar_codigo_qr, generar_pdf_entrada
import io

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Rutas de archivos de datos
EVENTOS_FILE = 'data/eventos.json'
COMPRAS_FILE = 'data/compras.json'

def cargar_eventos():
    """Carga eventos desde el archivo JSON"""
    if os.path.exists(EVENTOS_FILE):
        with open(EVENTOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def cargar_compras():
    """Carga compras desde el archivo JSON"""
    if os.path.exists(COMPRAS_FILE):
        with open(COMPRAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_eventos(eventos):
    """Guarda eventos en el archivo JSON"""
    with open(EVENTOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(eventos, f, indent=2, ensure_ascii=False)

def guardar_compras(compras):
    """Guarda compras en el archivo JSON"""
    with open(COMPRAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(compras, f, indent=2, ensure_ascii=False)

def obtener_asientos_ocupados(evento_id):
    """Obtiene lista de asientos ocupados para un evento desde compras.json"""
    compras = cargar_compras()
    asientos_ocupados = set()
    
    for compra in compras:
        if compra.get('evento_id') == evento_id and compra.get('asientos'):
            # Agregar cada asiento de esta compra al conjunto
            for asiento in compra['asientos']:
                asientos_ocupados.add(asiento)
    
    return list(asientos_ocupados)

def generar_mapa_asientos_interactivo(evento_id):
    """Genera mapa de asientos con estado real desde compras.json"""
    asientos_ocupados = obtener_asientos_ocupados(evento_id)
    filas = 10
    columnas = 15
    mapa = []
    
    for fila_idx in range(filas):
        fila_letra = chr(65 + fila_idx)  # A, B, C, ...
        for col_idx in range(columnas):
            numero_asiento = col_idx + 1  # 1, 2, 3, ...
            codigo_asiento = f"{fila_letra}{numero_asiento}"
            
            mapa.append({
                'codigo': codigo_asiento,
                'fila': fila_letra,
                'columna': numero_asiento,
                'ocupado': codigo_asiento in asientos_ocupados
            })
    
    return mapa

@app.route('/')
def index():
    """Página principal - Lista de eventos"""
    eventos = cargar_eventos()
    return render_template('index.html', eventos=eventos)

@app.route('/evento/<int:evento_id>')
def evento_detalle(evento_id):
    """Página de detalle del evento"""
    eventos = cargar_eventos()
    evento = next((e for e in eventos if e['id'] == evento_id), None)
    
    if not evento:
        return redirect(url_for('index'))
    
    return render_template('evento_detalle.html', evento=evento)

@app.route('/comprar/<int:evento_id>', methods=['GET', 'POST'])
def comprar(evento_id):
    """Página de compra de entrada con selección de asientos"""
    eventos = cargar_eventos()
    evento = next((e for e in eventos if e['id'] == evento_id), None)
    
    if not evento:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        asientos_seleccionados = request.form.getlist('asientos')
        
        # Si vienen como una lista vacía, intenta obtenerlos del formulario
        if not asientos_seleccionados:
            asientos_str = request.form.get('asientos', '')
            if asientos_str:
                asientos_seleccionados = asientos_str.split(',')
        
        # Limpiar y filtrar asientos vacíos
        asientos_seleccionados = [a.strip() for a in asientos_seleccionados if a.strip()]
        
        # Validaciones
        if not nombre or not correo:
            mapa_asientos = generar_mapa_asientos_interactivo(evento_id)
            return render_template('comprar.html', 
                                 evento=evento, 
                                 mapa_asientos=mapa_asientos,
                                 error='Por favor completa nombre y correo')
        
        if not asientos_seleccionados:
            mapa_asientos = generar_mapa_asientos_interactivo(evento_id)
            return render_template('comprar.html', 
                                 evento=evento, 
                                 mapa_asientos=mapa_asientos,
                                 error='Por favor selecciona al menos un asiento')
        
        # Validar que los asientos seleccionados sean válidos
        asientos_ocupados = obtener_asientos_ocupados(evento_id)
        for asiento in asientos_seleccionados:
            if asiento in asientos_ocupados:
                mapa_asientos = generar_mapa_asientos_interactivo(evento_id)
                return render_template('comprar.html', 
                                     evento=evento, 
                                     mapa_asientos=mapa_asientos,
                                     error=f'El asiento {asiento} ya está ocupado. Por favor elige otro.')
        
        # Validar cantidad vs entradas disponibles
        if len(asientos_seleccionados) > evento['entradas_disponibles']:
            mapa_asientos = generar_mapa_asientos_interactivo(evento_id)
            return render_template('comprar.html', 
                                 evento=evento, 
                                 mapa_asientos=mapa_asientos,
                                 error='No hay suficientes entradas disponibles')
        
        # Restar entradas disponibles
        evento['entradas_disponibles'] -= len(asientos_seleccionados)
        guardar_eventos(eventos)
        
        # Registrar compra
        compras = cargar_compras()
        nueva_compra = {
            'id': len(compras) + 1,
            'evento_id': evento_id,
            'evento_nombre': evento['nombre'],
            'nombre': nombre,
            'correo': correo,
            'cantidad': len(asientos_seleccionados),
            'precio_unitario': evento['precio'],
            'total': evento['precio'] * len(asientos_seleccionados),
            'fecha_compra': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'codigo_qr': f"ENTRADA-{len(compras) + 1}-{evento_id}",
            'asientos': sorted(asientos_seleccionados)  # Guardar asientos reales seleccionados
        }
        compras.append(nueva_compra)
        guardar_compras(compras)
        
        return render_template('compra_exitosa.html', compra=nueva_compra, evento=evento)
    
    # GET: Mostrar formulario con mapa de asientos
    mapa_asientos = generar_mapa_asientos_interactivo(evento_id)
    return render_template('comprar.html', evento=evento, mapa_asientos=mapa_asientos)

@app.route('/asientos/<int:evento_id>')
def ver_asientos(evento_id):
    """Página para ver mapa de asientos del evento"""
    eventos = cargar_eventos()
    evento = next((e for e in eventos if e['id'] == evento_id), None)
    
    if not evento:
        return redirect(url_for('index'))
    
    # Generar mapa de asientos interactivo con datos reales
    mapa_asientos = generar_mapa_asientos_interactivo(evento_id)
    
    total_asientos = len(mapa_asientos)
    ocupados = sum(1 for asiento in mapa_asientos if asiento['ocupado'])
    disponibles = total_asientos - ocupados
    
    # Reorganizar en formato de filas para la plantilla
    mapa_filas = {}
    for asiento in mapa_asientos:
        fila = asiento['fila']
        if fila not in mapa_filas:
            mapa_filas[fila] = []
        mapa_filas[fila].append(asiento)
    
    return render_template('asientos.html', 
                         evento=evento, 
                         mapa_filas=mapa_filas,
                         total_asientos=total_asientos,
                         ocupados=ocupados,
                         disponibles=disponibles)

@app.route('/descargar-entrada/<int:compra_id>')
def descargar_entrada(compra_id):
    """Descarga PDF de entrada"""
    compras = cargar_compras()
    compra = next((c for c in compras if c['id'] == compra_id), None)
    
    if not compra:
        return redirect(url_for('index'))
    
    eventos = cargar_eventos()
    evento = next((e for e in eventos if e['id'] == compra['evento_id']), None)
    
    if not evento:
        return redirect(url_for('index'))
    
    # Crear directorio temporal si no existe
    os.makedirs('app/temp', exist_ok=True)
    
    # Generar PDF
    pdf_path = f"app/temp/entrada_{compra_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    generar_pdf_entrada(compra, evento, pdf_path)
    
    # Descargar archivo
    return send_file(pdf_path, as_attachment=True, download_name=f"entrada_{compra['evento_nombre'].replace(' ', '_')}.pdf")

@app.route('/api/asientos/<int:evento_id>')
def api_asientos(evento_id):
    """API para obtener mapa de asientos con estado real"""
    mapa_asientos = generar_mapa_asientos_interactivo(evento_id)
    
    asientos_json = [
        {
            'codigo': a['codigo'],
            'fila': a['fila'],
            'columna': a['columna'],
            'ocupado': a['ocupado']
        }
        for a in mapa_asientos
    ]
    
    total = len(asientos_json)
    ocupados = sum(1 for a in asientos_json if a['ocupado'])
    disponibles = total - ocupados
    
    return jsonify({
        'evento_id': evento_id,
        'total_asientos': total,
        'ocupados': ocupados,
        'disponibles': disponibles,
        'asientos': asientos_json
    })

@app.route('/historial')
def historial():
    """Página de historial de compras"""
    compras = cargar_compras()
    return render_template('historial.html', compras=compras)

@app.route('/api/evento/<int:evento_id>')
def api_evento(evento_id):
    """API para obtener datos de un evento (JSON)"""
    eventos = cargar_eventos()
    evento = next((e for e in eventos if e['id'] == evento_id), None)
    
    if evento:
        return jsonify(evento)
    return jsonify({'error': 'Evento no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)

