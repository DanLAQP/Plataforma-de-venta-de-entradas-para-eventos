# 🚀 INICIO RÁPIDO - EventosPlatforma v2.0

## ⚡ Paso 1: Instalar dependencias

Abre la terminal/PowerShell en la carpeta del proyecto:

```bash
pip install -r requirements.txt
```

### Dependencias que se instalarán:
- Flask (servidor web)
- qrcode (generación de códigos QR)
- Pillow (procesamiento de imágenes)
- ReportLab (generación de PDFs)

## 🎬 Paso 2: Ejecutar la aplicación

### Opción 1: Windows (Recomendado)
Haz doble clic en `run.bat` o ejecuta:
```bash
python app.py
```

### Opción 2: macOS/Linux
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

## 🎫 Flujo de Prueba Recomendado

### 1. Ver Eventos
Accede a `http://localhost:5000/` y observa los eventos disponibles.

### 2. Ver Mapa de Asientos
Haz clic en "Ver Mapa de Asientos" para visualizar:
- Pantalla/Escenario
- Asientos disponibles (verde)
- Asientos ocupados (rojo)
- Estadísticas de ocupación

### 3. Comprar Entrada
Haz clic en "Comprar Entrada" y completa:
- Nombre
- Correo electrónico
- Cantidad de entradas

### 4. Descargar PDF
En la página de confirmación:
- Verás tus asientos asignados
- Podrás descargar tu entrada en PDF con código QR

### 5. Ver Historial
En la sección "Historial":
- Ve todas tus compras
- Revisa los asientos asignados
- Descarga PDFs de entradas anteriores

## 📋 Rutas principales

| Ruta | Descripción |
|------|-------------|
| `/` | Página principal - Ver todos los eventos |
| `/evento/1` | Detalle del evento |
| `/asientos/1` | Mapa de asientos (⭐ NUEVO) |
| `/comprar/1` | Formulario para comprar entrada |
| `/descargar-entrada/1` | Descargar entrada PDF (⭐ NUEVO) |
| `/historial` | Ver todas las compras |

## 📊 Datos Incluidos

La aplicación viene con 4 eventos de ejemplo:
1. **Festival de Música 2026** - $45 por entrada
2. **Conferencia de Tecnología** - $25 por entrada
3. **Concierto de Rock** - $55 por entrada
4. **Expo de Arte Contemporáneo** - $15 por entrada

## 📝 Agregar nuevos eventos

Ejecuta el script interactivo:

```bash
python add_event.py
```

Te pedirá:
- Nombre del evento
- Fecha (YYYY-MM-DD)
- Ubicación
- Precio por entrada
- Cantidad de entradas
- URL de imagen (opcional)
- Descripción

## 📥 Descargar Entradas

Las entradas descargables incluyen:
- Nombre del evento y fecha
- Datos del comprador
- Asientos asignados
- Código QR único
- Código de referencia

Los PDFs se guardan como:
```
entrada_[NombreEvento].pdf
```

## 📱 Características de la v2.0

### Códigos QR
```
ENTRADA-{id_compra}-{id_evento}
```

### Mapa de Asientos
- Grilla: 10 filas × 15 columnas = 150 asientos
- Colores: Verde (disponible), Rojo (ocupado)
- Asignación automática al comprar

### PDFs Descargables
- Información profesional
- Código QR integrado
- Asientos asignados
- Código único de entrada

## 🔧 Solución de problemas

### Error: "No module named 'qrcode'"
```bash
pip install qrcode[pil] pillow reportlab
```

### Error: "Port 5000 already in use"
Cambia el puerto en `app.py`:
```python
app.run(debug=True, port=5001)  # Usa otro puerto
```

### Los PDFs no se descargan
- Verifica permisos de escritura en la carpeta `app/`
- La carpeta `app/temp/` se crea automáticamente

### El mapa de asientos no se ve
- Limpia caché: `Ctrl+Shift+Delete`
- Recarga la página: `Ctrl+F5`

## 📁 Estructura de archivos

```
app/
├── app.py              ← Inicio aquí
├── add_event.py
├── requirements.txt    ← Instala primero
├── run.bat / run.sh    ← Ejecuta la app
├── app/
│   ├── templates/      ← Páginas HTML
│   ├── static/         ← CSS y JavaScript
│   └── utils.py        ← QR, PDF, asientos
└── data/
    ├── eventos.json
    └── compras.json
```

## 🎯 Próximos pasos

1. **Personaliza eventos**: Usa `python add_event.py`
2. **Modifica estilos**: Edita `app/static/css/style.css`
3. **Mejora JavaScript**: Edita `app/static/js/script.js`
4. **Prueba la API**: Accede a `/api/asientos/1`
5. **Sube a producción**: Usa Heroku, PythonAnywhere, etc.

## 📚 Recursos Adicionales

- [README.md](README.md) - Documentación completa
- [CHANGELOG.md](CHANGELOG.md) - Historial de cambios
- [Flask Documentation](https://flask.palletsprojects.com/)
- [QRCode Library](https://github.com/lincolnloop/python-qrcode)
- [ReportLab](https://www.reportlab.com/docs/reportlab-userguide.pdf)

## 🆘 Necesitas ayuda?

1. Revisa el archivo [README.md](README.md)
2. Consulta el [CHANGELOG.md](CHANGELOG.md)
3. Verifica los logs en la terminal
4. Prueba con `python app.py` en modo debug

---

¡Listo! 🎉 Tu plataforma de venta de entradas está lista para usar.

**Versión:** 2.0.0
**Última actualización:** 2026-05-24

