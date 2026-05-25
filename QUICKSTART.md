# 🚀 INICIO RÁPIDO - EventosPlatforma

## ⚡ Paso 1: Instalar dependencias

Abre la terminal/PowerShell en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

## 🎬 Paso 2: Ejecutar la aplicación

### Opción 1: Windows (Recomendado)
Haz doble clic en `run.bat` o ejecuta en PowerShell:
```bash
python app.py
```

### Opción 2: macOS/Linux
Ejecuta en terminal:
```bash
bash run.sh
```

O manualmente:
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## 🌐 Paso 3: Acceder a la aplicación

Abre tu navegador en:
```
http://localhost:5000/
```

## 📋 Rutas principales

| Ruta | Descripción |
|------|-------------|
| `/` | Página principal - Ver todos los eventos |
| `/evento/1` | Detalle del evento con ID 1 |
| `/comprar/1` | Formulario para comprar entrada del evento 1 |
| `/historial` | Ver todas las compras realizadas |

## 📝 Agregar nuevos eventos

Ejecuta el script interactivo en la terminal:

```bash
python add_event.py
```

Te pedirá información sobre el evento y lo añadirá automáticamente.

## 📊 Datos

Los datos se guardan automáticamente en archivos JSON:
- **eventos.json** - Contiene todos los eventos
- **compras.json** - Contiene todas las compras realizadas

Puedes editarlos directamente o usar el script `add_event.py`

## ✨ Características del MVP

✅ Ver lista de eventos con:
  - Nombre
  - Fecha
  - Ubicación
  - Precio
  - Imagen
  - Botón "Comprar Entrada"

✅ Ver detalles del evento:
  - Descripción completa
  - Entradas disponibles
  - Precio
  - Opción de compra

✅ Comprar entrada con:
  - Formulario simple (nombre, correo, cantidad)
  - Validación de datos
  - Reducción automática de stock

✅ Historial de compras:
  - Tabla con todas las compras
  - Resumen de gastos totales

✅ Interfaz moderna:
  - Diseño responsive con Bootstrap
  - Estilos personalizados
  - Animaciones suaves
  - Mejoras de UX con JavaScript

## 🛑 Detener la aplicación

Presiona `Ctrl+C` en la terminal

## ❓ Solución de problemas

### "python: command not found"
Python no está instalado. Descárgalo desde https://www.python.org/downloads/

### "No module named 'flask'"
Asegúrate de haber instalado las dependencias:
```bash
pip install -r requirements.txt
```

### Error "Port 5000 already in use"
El puerto 5000 está ocupado. Cambia el puerto en `app.py`:
```python
app.run(debug=True, port=5001)  # Usa otro puerto
```

### Los datos no se guardan
Verifica que las carpetas `data/`, `app/templates/` y `app/static/` existan

## 📚 Estructura de archivos

```
├── app.py                    # Backend (Flask)
├── add_event.py             # Script para agregar eventos
├── requirements.txt         # Dependencias
├── run.bat / run.sh         # Scripts de inicio
├── README.md                # Documentación
├── app/
│   ├── templates/           # Plantillas HTML
│   └── static/              # CSS y JavaScript
└── data/
    ├── eventos.json         # Base de datos de eventos
    └── compras.json         # Registro de compras
```

## 🎯 Próximos pasos

Después de tener el MVP funcionando, puedes:

1. **Agregar más eventos** usando `python add_event.py`
2. **Personalizar estilos** en `app/static/css/style.css`
3. **Mejorar interactividad** en `app/static/js/script.js`
4. **Agregar validación email** en el formulario
5. **Implementar autenticación** de usuarios
6. **Integrar pasarela de pagos** (Stripe, PayPal)
7. **Cambiar a base de datos real** (PostgreSQL, MySQL)

---

¡Listo! 🎉 Tu plataforma de venta de entradas está lista para usar.

¿Necesitas ayuda? Revisa el archivo README.md para más detalles.
