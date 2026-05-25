# 📋 CHANGELOG

## [v2.0.0] - 2026-05-24 - Mejoras Principales

### ✨ Nuevas Características

- **Códigos QR** - Generación automática de códigos QR para cada entrada
- **Mapa de Asientos** - Visualización interactiva de asientos con estados (disponible/ocupado)
- **Descarga de PDF** - Entradas en formato PDF con código QR incluido
- **Asientos Simulados** - Asignación automática de asientos al comprar
- **API REST** - Nuevos endpoints para obtener datos en JSON
  - `/api/asientos/<evento_id>` - Datos del mapa de asientos

### 🔧 Cambios Técnicos

- Nuevas dependencias:
  - `qrcode[pil]` 7.4.2
  - `pillow` 10.0.0
  - `reportlab` 4.0.7

- Nuevo módulo: `app/utils.py`
  - Función `generar_codigo_qr()`
  - Función `generar_pdf_entrada()`
  - Función `generar_mapa_asientos()`

- Nuevos templates:
  - `asientos.html` - Visualización del mapa de asientos

- Nuevas rutas Flask:
  - `GET /asientos/<evento_id>` - Ver mapa de asientos
  - `GET /descargar-entrada/<compra_id>` - Descargar PDF
  - `GET /api/asientos/<evento_id>` - API de asientos

- Mejoras en estructura de datos de compras:
  - Nuevo campo: `codigo_qr`
  - Nuevo campo: `asientos` (lista de asientos asignados)

### 🎨 Cambios en UI/UX

- Nuevo template `asientos.html` con mapa visual
- Actualizado `evento_detalle.html` con botón "Ver Mapa de Asientos"
- Actualizado `compra_exitosa.html` con:
  - Visualización de asientos asignados
  - Botón para descargar entrada en PDF
- Actualizado `historial.html` con:
  - Vista de tarjetas (cards) en lugar de tabla
  - Mostrar asientos de cada compra
  - Botón para descargar PDF desde historial

- Estilos CSS nuevos en `style.css`:
  - `.mapa-asientos-container` - Contenedor principal
  - `.pantalla` - Representación de pantalla/escenario
  - `.asiento` - Estilos individuales de asiento
  - `.asiento.disponible` - Asientos verdes disponibles
  - `.asiento.ocupado` - Asientos rojos ocupados
  - Animaciones y transiciones mejoradas

### 📦 Cambios en Archivos

- `requirements.txt` - Actualizadas dependencias
- `app.py` - Nuevas rutas y funcionalidades
- `app/__init__.py` - Creado como inicializador
- `app/utils.py` - Nuevo módulo de utilidades
- `app/static/css/style.css` - Estilos para mapa de asientos
- `app/static/js/script.js` - Scripts mejorados
- `README.md` - Documentación actualizada

### 🐛 Correcciones de Bugs

- Mejora en manejo de errores en generación de PDFs
- Validaciones mejoradas en compra de entradas

### 📊 Estructura de Datos

**Compra actualizada:**
```json
{
  "id": 1,
  "evento_id": 1,
  "evento_nombre": "Festival de Música 2026",
  "nombre": "Juan Pérez",
  "correo": "juan@ejemplo.com",
  "cantidad": 2,
  "precio_unitario": 45.00,
  "total": 90.00,
  "fecha_compra": "2026-05-24 14:30:00",
  "codigo_qr": "ENTRADA-1-1",
  "asientos": ["A1", "A2"]
}
```

### 🚀 Rendimiento

- Generación de PDFs optimizada
- Códigos QR cachados en memoria antes de PDF
- Mapa de asientos con 150 posiciones (10x15)

---

## [v1.0.0] - 2026-05-24 - MVP Inicial

### ✨ Características

- Ver listado de eventos
- Ver detalle de evento
- Comprar entradas
- Historial de compras
- Base de datos JSON
- Diseño responsive con Bootstrap
- JavaScript para mejorar UX

### 📦 Dependencias

- Flask 3.0.0
- Werkzeug 3.0.1

---

## Próximas Versiones Planeadas

- [ ] v2.1.0 - Autenticación de usuarios
- [ ] v2.2.0 - Integración de pasarelas de pago
- [ ] v2.3.0 - Envío de correos electrónicos
- [ ] v3.0.0 - Base de datos relacional
- [ ] v3.1.0 - Dashboard administrativo
