from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime

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
    """Página de compra de entrada"""
    eventos = cargar_eventos()
    evento = next((e for e in eventos if e['id'] == evento_id), None)
    
    if not evento:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        cantidad = int(request.form.get('cantidad', 0))
        
        # Validaciones
        if not nombre or not correo or cantidad <= 0:
            return render_template('comprar.html', evento=evento, error='Completa todos los campos correctamente')
        
        if cantidad > evento['entradas_disponibles']:
            return render_template('comprar.html', evento=evento, error='No hay suficientes entradas disponibles')
        
        # Restar entradas disponibles
        evento['entradas_disponibles'] -= cantidad
        guardar_eventos(eventos)
        
        # Registrar compra
        compras = cargar_compras()
        nueva_compra = {
            'id': len(compras) + 1,
            'evento_id': evento_id,
            'evento_nombre': evento['nombre'],
            'nombre': nombre,
            'correo': correo,
            'cantidad': cantidad,
            'precio_unitario': evento['precio'],
            'total': evento['precio'] * cantidad,
            'fecha_compra': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        compras.append(nueva_compra)
        guardar_compras(compras)
        
        return render_template('compra_exitosa.html', compra=nueva_compra)
    
    return render_template('comprar.html', evento=evento)

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
