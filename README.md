# 🎫 EventosPlatforma - MVP

Una plataforma simple para la venta de entradas de eventos construida con Flask, HTML, CSS y Bootstrap.

## Características

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
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
├── app/
│   ├── templates/             # Plantillas HTML
│   │   ├── base.html          # Template base con navegación
│   │   ├── index.html         # Página principal (lista de eventos)
│   │   ├── evento_detalle.html # Detalle del evento
│   │   ├── comprar.html       # Formulario de compra
│   │   ├── compra_exitosa.html # Confirmación de compra
│   │   └── historial.html     # Historial de compras
│   └── static/
│       ├── css/
│       │   └── style.css      # Estilos personalizados
│       └── js/
│           └── script.js      # JavaScript para mejorar UX
└── data/
    ├── eventos.json           # Base de datos de eventos
    └── compras.json           # Registro de compras realizadas
```

## Requisitos

- Python 3.7+
- Flask 3.0.0
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

La aplicación estará disponible en `http://localhost:5000/`

### Rutas disponibles
- `/` - Página principal (lista de eventos)
- `/evento/<id>` - Detalle del evento
- `/comprar/<id>` - Formulario de compra
- `/compra-exitosa` - Confirmación de compra
- `/historial` - Historial de compras
- `/api/evento/<id>` - API para obtener datos en JSON

## Flujo Principal

1. **Ver Eventos** 
   - El usuario accede a la página principal
   - Ve una tarjeta con cada evento (nombre, fecha, ubicación, precio, imagen)

2. **Ver Detalle del Evento**
   - Hace clic en "Ver Detalles"
   - Ve información completa del evento (descripción, entradas disponibles)

3. **Comprar Entrada**
   - Hace clic en "Comprar Entrada"
   - Rellena un formulario simple (nombre, correo, cantidad)
   - El sistema valida que haya stock disponible
   - Se registra la compra y disminuye el stock

4. **Historial de Compras**
   - Puede ver todas sus compras realizadas en una tabla
   - Se muestra resumen de total gastado

## Datos

### Eventos (data/eventos.json)
```json
{
  "id": 1,
  "nombre": "Festival de Música 2026",
  "fecha": "2026-06-15",
  "ubicacion": "Estadio Nacional",
  "precio": 45.00,
  "entradas_disponibles": 500,
  "imagen": "https://via.placeholder.com/400x300",
  "descripcion": "Gran festival de música..."
}
```

### Compras (data/compras.json)
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
  "fecha_compra": "2026-05-24 14:30:00"
}
```

## Funcionalidades Implementadas

✅ Ver listado de eventos
✅ Ver detalle de cada evento
✅ Comprar entradas con formulario
✅ Validación de formularios
✅ Reducción automática de stock
✅ Registro de compras en JSON
✅ Historial de compras
✅ Responsive design con Bootstrap
✅ Interfaz moderna con CSS personalizado
✅ Mejoras de UX con JavaScript

## Extensiones Posibles

- 🔐 Autenticación de usuarios
- 💳 Integración con pasarelas de pago (Stripe, PayPal)
- 📧 Envío de correos de confirmación
- ⭐ Sistema de reseñas
- 🔍 Búsqueda y filtrado de eventos
- 📊 Dashboard administrativo
- 🗄️ Base de datos relacional (PostgreSQL/MySQL)
- 🔔 Notificaciones en tiempo real

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autor

Creado como MVP para plataforma de venta de entradas para eventos.

---

¡Disfruta usando EventosPlatforma! 🎉
