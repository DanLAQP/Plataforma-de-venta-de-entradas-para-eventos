🚀 GUÍA DE INICIO RÁPIDO - EventosPlatforma v2.1
===============================================

OPCIÓN 1: INICIO AUTOMÁTICO (RECOMENDADO)
==========================================

Windows:
  1. Abre PowerShell en la carpeta del proyecto
  2. Ejecuta: .\setup.bat
  3. Se instalará todo automáticamente
  4. Abre navegador: http://localhost:5000/

Linux/macOS:
  1. Abre terminal en la carpeta del proyecto
  2. Ejecuta: python init.py
  3. Sigue las instrucciones
  4. Abre navegador: http://localhost:5000/


OPCIÓN 2: INICIO MANUAL
=======================

Paso 1: Instalar dependencias
  $ pip install -r requirements.txt

Paso 2: Resetear datos (opcional pero recomendado)
  $ python reset_data.py

Paso 3: Ejecutar aplicación
  $ python app.py

Paso 4: Abre navegador
  http://localhost:5000/


ESTRUCTURA DE CARPETAS
======================

plataforma_eventos/
├── app.py                           ← Aplicación Flask
├── requirements.txt                 ← Dependencias
├── data/
│   ├── eventos.json                 ← Eventos
│   └── compras.json                 ← Compras y asientos
├── app/
│   ├── __init__.py
│   ├── utils.py                     ← Funciones QR, PDF
│   ├── templates/
│   │   ├── base.html                ← Plantilla base
│   │   ├── index.html               ← Página principal
│   │   ├── evento_detalle.html      ← Detalle evento
│   │   ├── comprar.html             ← Mapa y compra ⭐
│   │   ├── compra_exitosa.html      ← Confirmación
│   │   ├── historial.html           ← Historial
│   │   └── asientos.html            ← Mapa de asientos
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css            ← Estilos
│   │   ├── js/
│   │   │   └── script.js            ← JavaScript
│   │   └── temp/                    ← PDFs temporales
├── scripts auxiliares
│   ├── install.py                   ← Instalación
│   ├── init.py                      ← Inicialización
│   ├── reset_data.py                ← Resetear datos
│   ├── verify.py                    ← Verificar
│   ├── cleanup.py                   ← Limpiar
│   ├── add_event.py                 ← Agregar eventos
├── setup.bat                        ← Setup Windows
├── run.bat                          ← Ejecutar Windows
├── run.sh                           ← Ejecutar Unix
└── documentación
    ├── README.md                    ← Documentación completa
    ├── RESUMEN_v2.1.md              ← Resumen v2.1 ⭐
    ├── VERIFICACIÓN_REQUISITOS.md   ← Requisitos verificados ⭐
    └── ...más documentos


CARACTERÍSTICAS PRINCIPALES v2.1
================================

✨ SELECCIÓN DINÁMICA DE ASIENTOS
   • Mapa interactivo 10×15 asientos
   • Click para seleccionar
   • Resumen en tiempo real
   • Asientos en colores:
     - Verde: Disponible
     - Rojo: Ocupado
     - Azul: Seleccionado

🎟️ ESTADO REAL DE ASIENTOS
   • Solo ocupados los realmente comprados
   • Datos desde compras.json
   • Sin simulación

📋 VALIDACIONES
   • Nombre y correo no vacíos
   • Al menos un asiento seleccionado
   • Asientos disponibles
   • Evita compra de ocupados

🎯 FLUJO COMPLETO
   Ver eventos → Detalle → Comprar → 
   Seleccionar asientos → Confirmación → 
   PDF con asientos


URLS IMPORTANTES
================

Página Principal
  http://localhost:5000/

Evento Específico
  http://localhost:5000/evento/1

Comprar Entrada (NUEVA SELECCIÓN DINÁMICA)
  http://localhost:5000/comprar/1

Mapa de Asientos
  http://localhost:5000/asientos/1

Historial de Compras
  http://localhost:5000/historial

API de Asientos
  http://localhost:5000/api/asientos/1


PRUEBA RÁPIDA (ESCENARIO COMPLETO)
===================================

1. Accede a: http://localhost:5000/
   → Verás 4 eventos

2. Haz clic en "Festival de Música 2026"
   → Verás detalles del evento

3. Haz clic en "Comprar Entrada"
   URL: http://localhost:5000/comprar/1
   → AHORA VES MAPA INTERACTIVO ⭐
   → A1, A2 en ROJO (ocupados)
   → B1 en ROJO (ocupado)
   → Resto en VERDE (disponibles)

4. Haz clic en asientos verdes, ej: A3, A5
   → Se resaltan en AZUL
   → Resumen muestra: "A3 A5"
   → Total: $90.00

5. Completa:
   • Nombre: Tu nombre
   • Correo: tu@correo.com

6. Haz clic "Comprar Ahora"
   → Backend valida
   → Muestra confirmación con A3, A5

7. Haz clic "📥 Descargar Entrada PDF"
   → Se descarga PDF con tus asientos

8. Ve al historial:
   http://localhost:5000/historial
   → Verás tu compra con A3, A5

9. Intenta comprar A3 nuevamente
   → Error: "A3 ya está ocupado"


DATOS DE PRUEBA PRECARGADOS
============================

Evento 1: Festival de Música (asientos ocupados: A1, A2, B1)
Evento 2: Conferencia (asientos ocupados: ninguno)
Evento 3: Concierto (asientos ocupados: ninguno)
Evento 4: Expo Arte (asientos ocupados: A1)

Compra 1:
  • Evento: Festival (id 1)
  • Asientos: A1, A2
  • Comprador: Luis Daniel

Compra 2:
  • Evento: Expo Arte (id 4)
  • Asientos: A1
  • Comprador: Luis Daniel

Compra 3:
  • Evento: Festival (id 1)
  • Asientos: B1
  • Comprador: Juan Pérez


SOLUCIÓN DE PROBLEMAS
=====================

❌ Error "ModuleNotFoundError: No module named 'flask'"
   → Solución: pip install -r requirements.txt

❌ Error de puerto 5000 ya en uso
   → Opción 1: Cambiar puerto en app.py (línea final)
   → Opción 2: Cerrar otra aplicación que use 5000

❌ No puedo hacer clic en asientos
   → Verifica: JavaScript activo en navegador
   → Verifica: No hay errores en consola (F12)

❌ Asientos no muestran ocupación correcta
   → Solución: python reset_data.py
   → Luego: python app.py

❌ JSON no se guarda
   → Verifica: Carpeta data/ existe
   → Verifica: Permisos de escritura en carpeta
   → Verifica: compras.json tiene permisos

❌ PDF no descarga
   → Verifica: Carpeta app/temp/ existe
   → Si no existe: Se crea automáticamente


DESARROLLO Y DEBUGGING
======================

Ver Logs en Tiempo Real:
  • Ejecuta: python app.py
  • Verás logs en terminal mientras usas la app
  • Los errores aparecerán inmediatamente

Consola del Navegador (F12):
  • Abre DevTools (F12)
  • Pestaña Console
  • Verás errores de JavaScript aquí

Inspeccionar BD (JSON):
  • Abre: data/eventos.json
  • Abre: data/compras.json
  • Verifica estructura y asientos

Verificar Aplicación:
  $ python verify.py


COMANDOS ÚTILES
===============

Instalar dependencias:
  python -m pip install -r requirements.txt

Inicializar proyecto:
  python init.py

Resetear datos iniciales:
  python reset_data.py

Verificar instalación:
  python verify.py

Limpiar archivos temporales:
  python cleanup.py

Agregar nuevo evento:
  python add_event.py

Ejecutar aplicación:
  python app.py

Ejecutar en otra carpeta:
  python -m flask --app app run


TECNOLOGÍAS USADAS
==================

Backend:
  • Python 3.7+
  • Flask 3.0.0
  • JSON para base de datos

Frontend:
  • HTML5
  • CSS3 (con Bootstrap 5)
  • JavaScript puro

Librerías Adicionales:
  • qrcode[pil] - Generación de códigos QR
  • Pillow - Procesamiento de imágenes
  • reportlab - Generación de PDFs
  • Werkzeug - Servidor WSGI


NAVEGADORES SOPORTADOS
======================

✅ Google Chrome / Chromium (Recomendado)
✅ Mozilla Firefox
✅ Apple Safari
✅ Microsoft Edge
✅ Opera
✅ Navegadores móviles modernos


REQUISITOS MÍNIMOS
==================

Python 3.7 o superior
  → Verificar: python --version

pip (gestor de paquetes)
  → Verificar: pip --version

Navegador moderno
  → Con JavaScript activo

Conexión a internet (opcional)
  → Solo para descargar dependencias


CONTACTO Y SOPORTE
==================

Documentación:
  • README.md - Guía completa
  • RESUMEN_v2.1.md - Cambios en v2.1
  • VERIFICACIÓN_REQUISITOS.md - Validación de requisitos

Errores conocidos:
  • Ninguno reportado en v2.1

Mejoras sugeridas:
  • Ver archivo README.md sección "Próximas mejoras"


PRÓXIMAS MEJORAS
================

v2.2 (Planeado):
  • Edición de compras
  • Cancelación de reservas
  • Email de confirmación
  • Dashboard de vendedor

v3.0 (Futuro):
  • Autenticación de usuarios
  • Integración de pagos (Stripe, PayPal)
  • Visualización 3D de escenario
  • Multi-idioma
  • Notificaciones en tiempo real


LICENCIA Y USO
==============

Este proyecto es de código abierto.
Úsalo libremente para:
  ✅ Aprendizaje
  ✅ Proyectos personales
  ✅ Desarrollo comercial

Crédito no requerido pero apreciado.


════════════════════════════════════════════════════════════
                   ¡YA ESTÁS LISTO!
════════════════════════════════════════════════════════════

Próximo paso:

Windows:  .\setup.bat
Linux:    python init.py  o  python app.py

Luego abre: http://localhost:5000/

¡Disfruta tu plataforma de venta de entradas! 🎉

════════════════════════════════════════════════════════════
