"""
Módulo para generar códigos QR y PDFs de entradas
"""

import qrcode
import io
import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from datetime import datetime

def generar_codigo_qr(datos, size=200):
    """
    Genera un código QR en memoria
    
    Args:
        datos (str): Datos a codificar en el QR
        size (int): Tamaño de la imagen en píxeles
    
    Returns:
        Image: Objeto PIL Image del código QR
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(datos)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Redimensionar si es necesario
    if img.size[0] != size:
        img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    return img

def generar_pdf_entrada(compra, evento, archivo_salida):
    """
    Genera un PDF de entrada con QR
    
    Args:
        compra (dict): Datos de la compra
        evento (dict): Datos del evento
        archivo_salida (str): Ruta donde guardar el PDF
    """
    # Crear documento PDF
    doc = SimpleDocTemplate(archivo_salida, pagesize=letter)
    elementos = []
    
    # Estilos
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#007bff'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#343a40'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # Generar código QR
    datos_qr = f"ENTRADA-{compra['id']}-{compra['evento_id']}"
    img_qr = generar_codigo_qr(datos_qr, size=250)
    
    # Guardar QR temporalmente
    qr_path = f"app/static/temp_qr_{compra['id']}.png"
    os.makedirs('app/static', exist_ok=True)
    img_qr.save(qr_path)
    
    # Título
    elementos.append(Paragraph("🎫 ENTRADA CONFIRMADA", titulo_style))
    elementos.append(Spacer(1, 0.3*inch))
    
    # Información principal
    datos_evento = [
        ['Evento:', evento['nombre']],
        ['Fecha:', evento['fecha']],
        ['Ubicación:', evento['ubicacion']],
    ]
    
    tabla_evento = Table(datos_evento, colWidths=[2*inch, 4*inch])
    tabla_evento.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    elementos.append(tabla_evento)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Información de comprador
    elementos.append(Paragraph("DATOS DEL COMPRADOR", heading_style))
    
    datos_comprador = [
        ['Nombre:', compra['nombre']],
        ['Correo:', compra['correo']],
        ['Cantidad de entradas:', str(compra['cantidad'])],
        ['Precio unitario:', f"${compra['precio_unitario']:.2f}"],
        ['Total:', f"${compra['total']:.2f}"],
    ]
    
    tabla_comprador = Table(datos_comprador, colWidths=[2*inch, 4*inch])
    tabla_comprador.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    elementos.append(tabla_comprador)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Código QR
    elementos.append(Paragraph("CÓDIGO QR DE ENTRADA", heading_style))
    elementos.append(Spacer(1, 0.2*inch))
    
    img_qr_reportlab = ReportLabImage(qr_path, width=2.5*inch, height=2.5*inch)
    
    # Centrar la imagen
    tabla_qr = Table([[img_qr_reportlab]], colWidths=[6*inch])
    tabla_qr.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    elementos.append(tabla_qr)
    
    elementos.append(Spacer(1, 0.2*inch))
    elementos.append(Paragraph(f"ID: {datos_qr}", ParagraphStyle(
        'CenteredSmall',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.grey
    )))
    
    elementos.append(Spacer(1, 0.3*inch))
    
    # Pie de página
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    elementos.append(Paragraph("---", footer_style))
    elementos.append(Spacer(1, 0.1*inch))
    elementos.append(Paragraph(
        f"Entrada generada: {datetime.now().strftime('%d/%m/%Y %H:%M')}<br/>Presenta este QR para acceder al evento",
        footer_style
    ))
    
    # Construir PDF
    doc.build(elementos)
    
    # Limpiar archivo temporal
    if os.path.exists(qr_path):
        os.remove(qr_path)
    
    return archivo_salida

def generar_mapa_asientos(filas=10, columnas=15, ocupados=None):
    """
    Genera un mapa de asientos simulado
    
    Args:
        filas (int): Número de filas
        columnas (int): Número de columnas
        ocupados (list): Lista de asientos ocupados [fila, columna]
    
    Returns:
        list: Matriz de asientos con estado
    """
    if ocupados is None:
        ocupados = []
    
    mapa = []
    for fila in range(filas):
        fila_asientos = []
        for col in range(columnas):
            numero_asiento = (fila * columnas) + col + 1
            # Crear asientos ocupados simulados aleatoriamente (10% de ocupación)
            ocupado = (fila, col) in ocupados or (numero_asiento % 10 == 0)
            fila_asientos.append({
                'numero': numero_asiento,
                'fila': chr(65 + fila),  # A, B, C...
                'columna': col + 1,
                'ocupado': ocupado
            })
        mapa.append(fila_asientos)
    
    return mapa

def asiento_a_codigo(fila, columna):
    """
    Convierte coordenadas a código de asiento
    
    Args:
        fila (int): Índice de fila
        columna (int): Índice de columna
    
    Returns:
        str: Código de asiento (ej: A1, B5)
    """
    return f"{chr(65 + fila)}{columna + 1}"
