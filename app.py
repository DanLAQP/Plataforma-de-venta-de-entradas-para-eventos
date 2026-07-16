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

# ====== FUNCIONES DE CARGA Y GUARDADO ======
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

# ====== FUNCIONES DE ZONAS Y PRECIOS ======
def obtener_zona_de_asiento(fila):
    """
    Obtiene la zona a la que pertenece un asiento según su fila.
    
    Args:
        fila (str): Letra de la fila (A-J)
    
    Returns:
        str: Nombre de la zona (VIP, PREFERENCIAL, GENERAL)
    """
    fila_upper = fila.upper()
    if fila_upper in ['A', 'B', 'C']:
        return 'VIP'
    elif fila_upper in ['D', 'E', 'F']:
        return 'PREFERENCIAL'
    else:
        return 'GENERAL'

def obtener_precio_asiento(evento_id, fila):
    """
    Obtiene el precio de un asiento según la zona del evento.
    
    Args:
        evento_id (int): ID del evento
        fila (str): Letra de la fila del asiento
    
    Returns:
        float: Precio del asiento
    """
    eventos = cargar_eventos()
    evento = next((e for e in eventos if e['id'] == evento_id), None)
    
    if not evento:
        return 0.0
    
    zona_nombre = obtener_zona_de_asiento(fila)
    zona = evento['zonas'].get(zona_nombre, {})
    return zona.get('precio', 0.0)

def obtener_eventos_por_mes(mes, año=2026):
    """
    Filtra los eventos por mes y año específicos.
    
    Args:
        mes (int): Número del mes (1-12)
        año (int): Año (por defecto 2026)
    
    Returns:
        list: Lista de eventos del mes especificado
    """
    eventos = cargar_eventos()
    eventos_filtrados = [
        evento for evento in eventos 
        if evento.get('mes') == mes and evento.get('año') == año
    ]
    return sorted(eventos_filtrados, key=lambda x: x.get('fecha', ''))

def obtener_meses_disponibles():
    """
    Obtiene lista única de meses con eventos disponibles.
    
    Returns:
        list: Lista de diccionarios con mes y año
    """
    eventos = cargar_eventos()
    meses = set()
    
    for evento in eventos:
        mes = evento.get('mes')
        año = evento.get('año')
        if mes and año:
            meses.add((mes, año))
    
    # Convertir a lista de diccionarios y ordenar
    meses_lista = [
        {'mes': mes, 'año': año} 
        for mes, año in sorted(meses)
    ]
    return meses_lista

def obtener_asientos_ocupados(evento_id):
    """
    Obtiene lista de asientos ocupados para un evento desde compras.json
    
    Args:
        evento_id (int): ID del evento
    
    Returns:
        list: Lista de códigos de asientos ocupados (ej: ['A1', 'A2', 'B5'])
    """
    compras = cargar_compras()
    asientos_ocupados = set()
    
    for compra in compras:
        if compra.get('evento_id') == evento_id and compra.get('asientos'):
            for asiento in compra['asientos']:
                asientos_ocupados.add(asiento)
    
    return list(asientos_ocupados)

def generar_mapa_asientos_interactivo(evento_id):
    """
    Genera mapa de asientos con información de zona y precio.
    
    Args:
        evento_id (int): ID del evento
    
    Returns:
        list: Lista de diccionarios con información de cada asiento
    """
    asientos_ocupados = obtener_asientos_ocupados(evento_id)
    filas = 10
    columnas = 15
    mapa = []
    
    for fila_idx in range(filas):
        fila_letra = chr(65 + fila_idx)  # A, B, C, ...
        for col_idx in range(columnas):
            numero_asiento = col_idx + 1  # 1, 2, 3, ...
            codigo_asiento = f"{fila_letra}{numero_asiento}"
            zona = obtener_zona_de_asiento(fila_letra)
            precio = obtener_precio_asiento(evento_id, fila_letra)
            
            mapa.append({
                'codigo': codigo_asiento,
                'fila': fila_letra,
                'columna': numero_asiento,
                'zona': zona,
                'precio': precio,
                'ocupado': codigo_asiento in asientos_ocupados
            })
    
    return mapa

def obtener_nombre_mes(mes):
    """
    Convierte número de mes a nombre en español.
    
    Args:
        mes (int): Número del mes (1-12)
    
    Returns:
        str: Nombre del mes en español
    """
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    return meses.get(mes, '')

@app.route('/')
def index():
    """Página principal - Lista de eventos con filtro por mes"""
    meses_disponibles = obtener_meses_disponibles()
    
    # Obtener mes seleccionado desde parámetro GET, si no existe usar el primero disponible
    mes_seleccionado = request.args.get('mes', type=int)
    
    if mes_seleccionado:
        eventos = obtener_eventos_por_mes(mes_seleccionado)
    else:
        eventos = cargar_eventos()
    
    # Crear información de meses para mostrar en template
    meses_info = []
    for m in meses_disponibles:
        meses_info.append({
            'numero': m['mes'],
            'nombre': obtener_nombre_mes(m['mes']),
            'año': m['año'],
            'seleccionado': m['mes'] == mes_seleccionado
        })
    
    return render_template('index.html', 
                         eventos=eventos, 
                         meses_disponibles=meses_info,
                         mes_seleccionado=mes_seleccionado)

@app.route('/evento/<int:evento_id>')
def evento_detalle(evento_id):
    """Página de detalle del evento"""
    eventos = cargar_eventos()
    evento = next((e for e in eventos if e['id'] == evento_id), None)
    
    if not evento:
        return redirect(url_for('index'))
    
    return render_template('evento_detalle.html', evento=evento)

def crear_compra(evento_id, nombre, correo, asientos_seleccionados):
    """
    Valida y registra una compra de entradas. Usada tanto por el formulario
    HTML (/comprar) como por la API REST (POST /api/compras).

    Returns:
        tuple: (compra, error, status_code). Si error es None, compra
        contiene el diccionario de la compra creada y status_code es 201.
        Si error no es None, compra es None y status_code es el código
        HTTP apropiado (400, 404 o 409).
    """
    eventos = cargar_eventos()
    evento = next((e for e in eventos if e['id'] == evento_id), None)

    if not evento:
        return None, 'Evento no encontrado', 404

    nombre = (nombre or '').strip()
    correo = (correo or '').strip()
    asientos_seleccionados = [a.strip() for a in (asientos_seleccionados or []) if a and a.strip()]

    if not nombre or not correo:
        return None, 'Por favor completa nombre y correo', 400

    if not asientos_seleccionados:
        return None, 'Por favor selecciona al menos un asiento', 400

    asientos_ocupados = obtener_asientos_ocupados(evento_id)
    for asiento in asientos_seleccionados:
        if asiento in asientos_ocupados:
            return None, f'El asiento {asiento} ya está ocupado. Por favor elige otro.', 409

    total_compra = 0.0
    for asiento in asientos_seleccionados:
        fila = asiento[0]  # Primera letra es la fila
        precio_asiento = obtener_precio_asiento(evento_id, fila)
        total_compra += precio_asiento

    compras = cargar_compras()
    precio_unitario = total_compra / len(asientos_seleccionados) if asientos_seleccionados else 0

    nueva_compra = {
        'id': len(compras) + 1,
        'evento_id': evento_id,
        'evento_nombre': evento['nombre'],
        'nombre': nombre,
        'correo': correo,
        'cantidad': len(asientos_seleccionados),
        'precio_unitario': precio_unitario,
        'total': total_compra,
        'fecha_compra': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'codigo_qr': f"ENTRADA-{len(compras) + 1}-{evento_id}",
        'asientos': sorted(asientos_seleccionados)
    }
    compras.append(nueva_compra)
    guardar_compras(compras)

    return nueva_compra, None, 201

@app.route('/comprar/<int:evento_id>', methods=['GET', 'POST'])
def comprar(evento_id):
    """Página de compra de entrada con selección de asientos por zona"""
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

        compra, error, _status = crear_compra(evento_id, nombre, correo, asientos_seleccionados)

        if error:
            mapa_asientos = generar_mapa_asientos_interactivo(evento_id)
            return render_template('comprar.html',
                                 evento=evento,
                                 mapa_asientos=mapa_asientos,
                                 error=error)

        return render_template('compra_exitosa.html', compra=compra, evento=evento)

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

@app.route('/historial')
def historial():
    """Página de historial de compras"""
    compras = cargar_compras()
    return render_template('historial.html', compras=compras)

# ====================================================================
# ===================  API REST  ====================================
# ====================================================================
# Recursos: /api/eventos, /api/eventos/<id>, /api/eventos/<id>/asientos,
#           /api/compras, /api/compras/<id>
# Todas las respuestas son JSON con códigos de estado HTTP estándar.
# ====================================================================

def construir_respuesta_asientos(evento_id):
    """Arma el JSON del mapa de asientos (estado, zona y precio) de un evento."""
    mapa_asientos = generar_mapa_asientos_interactivo(evento_id)

    asientos_json = [
        {
            'codigo': a['codigo'],
            'fila': a['fila'],
            'columna': a['columna'],
            'zona': a['zona'],
            'precio': a['precio'],
            'ocupado': a['ocupado']
        }
        for a in mapa_asientos
    ]

    total = len(asientos_json)
    ocupados = sum(1 for a in asientos_json if a['ocupado'])
    disponibles = total - ocupados

    return {
        'evento_id': evento_id,
        'total_asientos': total,
        'ocupados': ocupados,
        'disponibles': disponibles,
        'asientos': asientos_json
    }

@app.route('/api/eventos', methods=['GET', 'POST'])
def api_eventos():
    """Colección de eventos: listar (GET) o crear (POST)"""
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}

        campos_requeridos = ['nombre', 'tipo', 'fecha', 'hora', 'mes', 'año',
                              'ubicacion', 'ponente', 'descripcion',
                              'duracion_minutos', 'capacidad_total', 'zonas']
        faltantes = [c for c in campos_requeridos if c not in data]
        if faltantes:
            return jsonify({'error': f'Campos requeridos faltantes: {", ".join(faltantes)}'}), 400

        eventos = cargar_eventos()
        nuevo_id = max([e['id'] for e in eventos], default=0) + 1

        zonas = data['zonas']
        for zona in zonas.values():
            zona.setdefault('disponibles', zona.get('total_asientos', 0))

        nuevo_evento = {
            'id': nuevo_id,
            'nombre': data['nombre'],
            'tipo': data['tipo'],
            'fecha': data['fecha'],
            'hora': data['hora'],
            'mes': data['mes'],
            'año': data['año'],
            'ubicacion': data['ubicacion'],
            'ponente': data['ponente'],
            'descripcion': data['descripcion'],
            'imagen': data.get('imagen', ''),
            'duracion_minutos': data['duracion_minutos'],
            'capacidad_total': data['capacidad_total'],
            'asientos_vendidos': 0,
            'zonas': zonas,
            'estado': data.get('estado', 'disponible'),
            'fecha_creacion': datetime.now().isoformat()
        }
        eventos.append(nuevo_evento)
        guardar_eventos(eventos)
        return jsonify(nuevo_evento), 201

    # GET: listar eventos, con filtro opcional ?mes=&año=
    mes = request.args.get('mes', type=int)
    if mes:
        año = request.args.get('año', type=int, default=2026)
        eventos = obtener_eventos_por_mes(mes, año)
    else:
        eventos = cargar_eventos()
    return jsonify(eventos)

@app.route('/api/eventos/<int:evento_id>', methods=['GET', 'PUT', 'DELETE'])
def api_evento_detalle(evento_id):
    """Recurso individual de evento: obtener (GET), actualizar (PUT) o eliminar (DELETE)"""
    eventos = cargar_eventos()
    evento = next((e for e in eventos if e['id'] == evento_id), None)

    if not evento:
        return jsonify({'error': 'Evento no encontrado'}), 404

    if request.method == 'GET':
        return jsonify(evento)

    if request.method == 'PUT':
        data = request.get_json(silent=True) or {}
        campos_editables = ['nombre', 'tipo', 'fecha', 'hora', 'mes', 'año',
                             'ubicacion', 'ponente', 'descripcion', 'imagen',
                             'duracion_minutos', 'capacidad_total', 'zonas', 'estado']
        for campo in campos_editables:
            if campo in data:
                evento[campo] = data[campo]
        guardar_eventos(eventos)
        return jsonify(evento)

    # DELETE
    eventos = [e for e in eventos if e['id'] != evento_id]
    guardar_eventos(eventos)
    return '', 204

@app.route('/api/eventos/<int:evento_id>/asientos')
def api_evento_asientos(evento_id):
    """Mapa de asientos de un evento (estado, zona y precio de cada uno)"""
    eventos = cargar_eventos()
    if not any(e['id'] == evento_id for e in eventos):
        return jsonify({'error': 'Evento no encontrado'}), 404
    return jsonify(construir_respuesta_asientos(evento_id))

@app.route('/api/compras', methods=['GET', 'POST'])
def api_compras():
    """Colección de compras: listar (GET, filtrable por ?evento_id=) o crear (POST)"""
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}

        if 'evento_id' not in data:
            return jsonify({'error': 'evento_id es requerido'}), 400
        try:
            evento_id = int(data['evento_id'])
        except (TypeError, ValueError):
            return jsonify({'error': 'evento_id debe ser un número'}), 400

        asientos = data.get('asientos', [])
        if not isinstance(asientos, list):
            return jsonify({'error': 'asientos debe ser una lista de códigos (ej. ["A1", "A2"])'}), 400

        compra, error, status = crear_compra(evento_id, data.get('nombre'), data.get('correo'), asientos)
        if error:
            return jsonify({'error': error}), status
        return jsonify(compra), status

    # GET: listar compras, con filtro opcional ?evento_id=
    compras = cargar_compras()
    evento_id_filtro = request.args.get('evento_id', type=int)
    if evento_id_filtro is not None:
        compras = [c for c in compras if c.get('evento_id') == evento_id_filtro]
    return jsonify(compras)

@app.route('/api/compras/<int:compra_id>', methods=['GET', 'PUT', 'DELETE'])
def api_compra_detalle(compra_id):
    """Recurso individual de compra: obtener (GET), actualizar (PUT) o cancelar (DELETE)"""
    compras = cargar_compras()
    compra = next((c for c in compras if c['id'] == compra_id), None)
    if not compra:
        return jsonify({'error': 'Compra no encontrada'}), 404

    if request.method == 'GET':
        return jsonify(compra)

    if request.method == 'PUT':
        data = request.get_json(silent=True) or {}
        nombre = data.get('nombre', compra['nombre'])
        correo = data.get('correo', compra['correo'])
        asientos_nuevos = data.get('asientos')

        if not (nombre or '').strip() or not (correo or '').strip():
            return jsonify({'error': 'Por favor completa nombre y correo'}), 400

        if asientos_nuevos is not None:
            if not isinstance(asientos_nuevos, list) or not asientos_nuevos:
                return jsonify({'error': 'asientos debe ser una lista con al menos un asiento'}), 400
            asientos_nuevos = [a.strip() for a in asientos_nuevos if a and a.strip()]

            # Asientos ocupados por OTRAS compras del mismo evento (excluye esta compra)
            ocupados_otras = set()
            for c in compras:
                if c['id'] != compra_id and c.get('evento_id') == compra['evento_id']:
                    ocupados_otras.update(c.get('asientos', []))

            for asiento in asientos_nuevos:
                if asiento in ocupados_otras:
                    return jsonify({'error': f'El asiento {asiento} ya está ocupado. Por favor elige otro.'}), 409

            total = 0.0
            for asiento in asientos_nuevos:
                fila = asiento[0]
                total += obtener_precio_asiento(compra['evento_id'], fila)

            compra['asientos'] = sorted(asientos_nuevos)
            compra['cantidad'] = len(asientos_nuevos)
            compra['precio_unitario'] = total / len(asientos_nuevos)
            compra['total'] = total

        compra['nombre'] = nombre.strip()
        compra['correo'] = correo.strip()

        guardar_compras(compras)
        return jsonify(compra)

    # DELETE
    compras = [c for c in compras if c['id'] != compra_id]
    guardar_compras(compras)
    return '', 204

# --- Alias heredados (mantenidos por compatibilidad con versiones previas) ---

@app.route('/api/asientos/<int:evento_id>')
def api_asientos(evento_id):
    """[Deprecado] Usar /api/eventos/<id>/asientos"""
    return api_evento_asientos(evento_id)

@app.route('/api/evento/<int:evento_id>')
def api_evento(evento_id):
    """[Deprecado] Usar /api/eventos/<id>"""
    return api_evento_detalle(evento_id)

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)

