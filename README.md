# 🎫 EventosPlatforma - MVP Mejorado

Una plataforma moderna para la venta de entradas de eventos construida con Flask, HTML, CSS y Bootstrap. Ahora con códigos QR, mapa de asientos y PDFs descargables.

## ✨ Características Nuevas

✅ **Códigos QR** - Códigos QR únicos para cada entrada
✅ **Mapa de Asientos** - Visualización interactiva (verde disponible, rojo ocupado)
✅ **Descargar PDF** - Entradas en PDF con código QR incluido
✅ **Asientos Simulados** - Cada compra asigna asientos específicos
✅ **API REST** - Endpoints para obtener datos en JSON

## Características Originales

✅ **Ver eventos** - Página principal con listado de eventos disponibles
✅ **Detalle del evento** - Información completa de cada evento
✅ **Comprar entradas** - Formulario simple para comprar entradas
✅ **Historial de compras** - Ver todas tus compras realizadas
✅ **Gestión de stock** - Disminución automática de entradas disponibles
✅ **Base de datos JSON** - Datos almacenados en archivos JSON

## Estructura del Proyecto

```
Plataforma-de-venta-de-entradas-para-eventos/
├── app.py                      # Aplicación principal de Flask
├── add_event.py                # Script para agregar eventos
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
├── QUICKSTART.md               # Guía de inicio rápido
├── run.bat / run.sh            # Scripts ejecutables
├── app/
│   ├── utils.py               # Utilidades (QR, PDF, asientos)
│   ├── __init__.py            # Inicializador del módulo
│   ├── templates/             # Plantillas HTML
│   │   ├── base.html          # Template base
│   │   ├── index.html         # Página principal
│   │   ├── evento_detalle.html # Detalle del evento
│   │   ├── asientos.html      # Mapa de asientos ⭐ NUEVO
│   │   ├── comprar.html       # Formulario de compra
│   │   ├── compra_exitosa.html # Confirmación de compra
│   │   └── historial.html     # Historial de compras
│   └── static/
│       ├── css/
│       │   └── style.css      # Estilos (incl. mapa de asientos)
│       ├── js/
│       │   └── script.js      # JavaScript mejorado
│       └── temp/              # PDFs temporales
└── data/
    ├── eventos.json           # Base de datos de eventos
    └── compras.json           # Registro de compras
```

## Requisitos

- Python 3.7+
- Flask 3.0.0
- qrcode 7.4.2
- pillow (PIL) 10.0.0
- reportlab 4.0.7
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar el repositorio
```bash
cd "C:\Users\Computer\Desktop\plataforma_eventos\Plataforma-de-venta-de-entradas-para-eventos"
```

### 2. Crear un entorno virtual (recomendado)
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Uso

### Iniciar la aplicación
```bash
python app.py
```

O usar los scripts proporcionados:
- **Windows**: Haz doble clic en `run.bat`
- **macOS/Linux**: Ejecuta `bash run.sh`

La aplicación estará disponible en `http://localhost:5000/`

### Rutas disponibles

| Ruta | Descripción |
|------|-------------|
| `/` | Página principal (lista de eventos) |
| `/evento/<id>` | Detalle del evento |
| `/asientos/<id>` | Mapa de asientos del evento ⭐ NUEVO |
| `/comprar/<id>` | Formulario de compra |
| `/descargar-entrada/<id>` | Descarga PDF de entrada ⭐ NUEVO |
| `/historial` | Historial de compras |
| `/api/evento/<id>` | API JSON del evento |
| `/api/asientos/<id>` | API JSON del mapa de asientos ⭐ NUEVO |

## Características Nuevas - Detalles

### 1. Códigos QR
- Se generan automáticamente en cada compra
- Incluidos en el PDF descargable
- Formato: `ENTRADA-{id}-{evento_id}`

### 2. Mapa de Asientos
- Grilla interactiva de 10 filas × 15 columnas = 150 asientos
- Colores: Verde (disponible), Rojo (ocupado)
- Muestra estadísticas de ocupación
- Asignación automática de asientos al comprar

### 3. Descarga de PDF
- Documento profesional con:
  - Información del evento
  - Datos del comprador
  - Asientos asignados
  - Código QR
  - Código único de entrada
- Descargable desde confirmación de compra e historial

### 4. Estructura de Datos Mejorada

**Compra (compras.json)**
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

## Funcionalidades Implementadas

### Entradas
- [x] Página principal con listado
- [x] Detalle del evento
- [x] Compra con validaciones
- [x] Formulario simple (nombre, correo, cantidad)

### Asientos
- [x] Mapa visual de asientos
- [x] Estados (disponible/ocupado)
- [x] Asignación automática
- [x] Estadísticas de ocupación

### QR y PDF
- [x] Generación de código QR
- [x] PDF descargable
- [x] Datos completos en PDF
- [x] Código único por entrada

### Historial
- [x] Tabla de compras
- [x] Vista de tarjetas mejorada
- [x] Descargar entrada desde historial
- [x] Resumen de gastos

### UX/UI
- [x] Diseño responsive
- [x] Animaciones suaves
- [x] Bootstrap 5
- [x] JavaScript interactivo
- [x] Colores intuitivos

## Extensiones Posibles

- 🔐 Autenticación de usuarios
- 💳 Integración con pasarelas de pago
- 📧 Envío de correos con QR
- ⭐ Sistema de reseñas
- 🔍 Búsqueda y filtrado
- 📊 Dashboard administrativo
- 🗄️ Base de datos real (PostgreSQL)
- 🔔 Notificaciones en tiempo real
- 📱 App móvil
- 🌍 Multiidioma

## Solución de Problemas

### "No module named 'qrcode'"
```bash
pip install qrcode[pil] pillow reportlab
```

### "Port 5000 already in use"
Cambia el puerto en `app.py`:
```python
app.run(debug=True, port=5001)
```

### Error al generar PDF
Asegúrate de que la carpeta `app/temp` sea escribible o se cree automáticamente.

### Los asientos no se ven correctamente
Limpiar caché del navegador: `Ctrl+Shift+Delete`

## Licencia

Código abierto bajo licencia MIT.

## Autor

Creado como MVP mejorado para plataforma de venta de entradas para eventos.

---

¡Disfruta usando EventosPlatforma! 🎉

