📋 ACTUALIZACIÓN v2.1 - SELECCIÓN DINÁMICA DE ASIENTOS
====================================================

CAMBIOS PRINCIPALES
===================

✨ NUEVA FUNCIONALIDAD: SELECCIÓN DINÁMICA DE ASIENTOS
-----------------------------------------------------

Antes (v2.0):
  ❌ Los asientos se asignaban automáticamente (A1, A2, B1, etc.)
  ❌ No había opción para elegir asientos
  ❌ No se validaba si un asiento ya estaba ocupado
  ❌ Todos los asientos se marcaban ocupados por defecto

Ahora (v2.1):
  ✅ El usuario puede hacer clic en los asientos para seleccionarlos
  ✅ Solo aparecen ocupados los asientos realmente comprados
  ✅ Los asientos disponibles se muestran en verde
  ✅ Los asientos ocupados se muestran en rojo
  ✅ Sistema de validación para evitar compras de ocupados
  ✅ Resumen dinámico de asientos seleccionados


FLUJO DE COMPRA (NUEVO)
=======================

1. Usuario va a comprar entrada
   → Ve mapa interactivo de asientos

2. Usuario selecciona asientos haciendo clic
   → Asientos se resaltan en azul
   → Se actualiza cantidad y total en tiempo real

3. Usuario llena nombre y correo
   → Datos se validan

4. Usuario compra
   → Se valida que asientos no estén ocupados
   → Se guardan EXACTAMENTE los asientos seleccionados
   → Se actualiza JSON con asientos reales


CAMBIOS DE CÓDIGO
==================

1. Backend (app.py)
   ─────────────────
   ✅ Nueva función: obtener_asientos_ocupados(evento_id)
      → Lee compras.json y retorna asientos ocupados realmente

   ✅ Nueva función: generar_mapa_asientos_interactivo(evento_id)
      → Genera mapa 10x15 con estado real de cada asiento
      → Solo marca ocupados los que están en compras.json

   ✅ Actualización ruta POST /comprar/<id>
      → Recibe lista de asientos seleccionados (no cantidad)
      → Valida que asientos no estén ocupados
      → Guarda asientos EXACTOS en compra

   ✅ Actualización ruta GET /comprar/<id>
      → Pasa mapa_asientos al template con datos reales

   ✅ Actualización ruta GET /api/asientos/<id>
      → Retorna asientos con estado real desde JSON


2. Frontend (comprar.html)
   ──────────────────────
   ✅ Nuevo: Mapa interactivo de asientos en la página de compra
      → Grilla 10x15 con botones clickeables
      → Leyenda: Verde (disponible), Rojo (ocupado), Azul (seleccionado)
      → Pantalla visual al tope

   ✅ Nuevo: Sistema de selección por clic
      → Click = selecciona asiento (resalta en azul)
      → Click nuevamente = deselecciona

   ✅ Nuevo: Resumen de asientos seleccionados
      → Muestra badges con códigos de asientos
      → Se actualiza en tiempo real

   ✅ Nuevo: Campo oculto asientos
      → Envía array de asientos al servidor: asientos=A1,A2,B1

   ✅ Actualización cálculo de precio
      → Se basa en cantidad de asientos seleccionados (no en campo cantidad)


3. Datos JSON (data/compras.json)
   ────────────────────────────
   ✅ Campo "asientos" ahora contiene asientos REALES seleccionados
      Antes: ["A1", "A2"] (simulados)
      Ahora: ["A1", "A2"] (seleccionados por usuario)

   ✅ Todas las compras tienen asientos reales
      → Consistencia en datos


4. API REST
   ─────────
   ✅ GET /api/asientos/<evento_id>
      → Retorna JSON con asientos y estado REAL
      
      Respuesta:
      {
        "evento_id": 1,
        "total_asientos": 150,
        "ocupados": 3,
        "disponibles": 147,
        "asientos": [
          {"codigo": "A1", "ocupado": true, ...},
          {"codigo": "A2", "ocupado": false, ...},
          ...
        ]
      }


VALIDACIONES IMPLEMENTADAS
===========================

1. ✅ Nombre y correo no vacíos
   → Si faltan, se muestran errores claros

2. ✅ Al menos un asiento seleccionado
   → Error si no hay asientos seleccionados

3. ✅ Asientos no están ocupados
   → Valida servidor ANTES de guardar
   → Error si algún asiento ya fue comprado

4. ✅ Asientos válidos
   → Solo acepta códigos A1-J15

5. ✅ Cantidad no excede entradas disponibles
   → Valida contra total disponible


ESTRUCTURA DE ASIENTOS
======================

Formato: LetraNumero (ej: A1, B5, J15)

Filas (Letras):     A B C D E F G H I J (10 filas)
Columnas (Números): 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 (15 columnas)

Total asientos: 10 × 15 = 150 asientos


ARCHIVOS MODIFICADOS
====================

✏️  app.py
    • Nuevas funciones: obtener_asientos_ocupados(), 
                       generar_mapa_asientos_interactivo()
    • Actualizado: comprar() - recibe asientos, no cantidad
    • Actualizado: ver_asientos() - usa datos reales
    • Actualizado: api_asientos() - datos reales

✏️  app/templates/comprar.html
    • Completamente reescrito con mapa interactivo
    • Nuevo sistema de selección por clic
    • Nuevo resumen de asientos
    • Nuevo JavaScript para interactividad

✏️  app/templates/asientos.html
    • Actualizado para usar mapa_filas (datos reales)
    • Corregido iteración de asientos

✏️  data/compras.json
    • Normalizado: todas compras con asientos reales
    • Compra 1: A1, A2
    • Compra 2: A1 (evento 4)
    • Compra 3: B1

✏️  requirements.txt
    • Actualizado: qrcode[pil] (especifica PIL como dependencia)


ARCHIVOS NUEVOS
===============

📄 reset_data.py
   • Script para resetear datos iniciales
   • Crea eventos.json y compras.json consistentes
   • Útil para pruebas

📄 init.py
   • Script de inicialización completo
   • Instala dependencias
   • Crea directorios
   • Resetea datos
   • Verifica instalación


CÓMO PROBAR
===========

1. Instala dependencias:
   python -m pip install -r requirements.txt

2. Resetea datos (opcional):
   python reset_data.py

3. Ejecuta la app:
   python app.py

4. Ve a: http://localhost:5000/

5. Prueba el flujo:
   a) Haz clic en un evento
   b) Ve "🗺️ Ver Mapa de Asientos" para ver el mapa
   c) O ve directo a "Comprar Entrada"
   d) En la página de compra, haz clic en asientos verdes
   e) Verás resaltarse en azul y el total actualizar
   f) Completa nombre y correo
   g) Haz clic "Comprar"
   h) Verás confirmación con asientos reales


EJEMPLO DE USO
==============

Escenario: Comprar 2 entradas para Festival de Música

1. Ingreso a: http://localhost:5000/evento/1
2. Hago clic en "Comprar Entrada"
3. Veo mapa de asientos:
   - A1, A2: OCUPADOS (rojo) - comprados anteriormente
   - B1: OCUPADO (rojo) - comprado anteriormente
   - Resto: DISPONIBLES (verde)

4. Hago clic en asientos verdes: A3, A4
   - Se resaltan en azul
   - Resumen muestra: "A3 A4"
   - Total: $90.00 (2 × $45)

5. Completo:
   - Nombre: "Juan Pérez"
   - Correo: "juan@example.com"

6. Hago clic "Comprar Ahora"
   - Servidor valida: A3 y A4 disponibles ✅
   - Guarda compra con asientos: ["A3", "A4"]
   - Muestra confirmación

7. En historial aparece con asientos: A3, A4
   - Puedo descargar PDF con esos asientos


VENTAJAS DEL SISTEMA
====================

✅ Control total del usuario
   → Elige exactamente dónde quiere sentarse

✅ Datos consistentes
   → JSON siempre refleja asientos reales

✅ Sin errores de ocupación
   → Valida servidor para evitar dobles compras

✅ UX intuitiva
   → Mapa visual, click directo, feedback inmediato

✅ Flexible
   → Puede comprar 1, 2, 3... asientos
   → Elige cualquier combinación disponible

✅ Profesional
   → Los PDFs muestran asientos reales seleccionados
   → Confirmación clara


PREGUNTAS FRECUENTES
====================

P: ¿Qué pasa si alguien compra mientras estoy seleccionando?
R: Se valida en servidor ANTES de guardar. Si alguien compró
   el asiento que seleccionaste, recibirás error.

P: ¿Puedo cambiar mis asientos después de comprar?
R: No, pero puedes descargar el PDF con tus asientos reales.

P: ¿El sistema permite editar compras?
R: Actualmente no. Para modificar, necesitarías:
   1. Eliminar la compra manualmente de JSON
   2. Hacer nueva compra con asientos correctos

P: ¿Cuántos asientos puedo comprar?
R: Hasta 150 (todos). Solo no puedes comprar ocupados.

P: ¿Por qué algunos asientos salen ocupados desde el inicio?
R: Porque hay compras previas en compras.json. Puedes
   resetear datos con: python reset_data.py


COMPATIBILIDAD
==============

✅ Chrome/Chromium
✅ Firefox
✅ Safari
✅ Edge
✅ Navegadores móviles (responsive)

Requisitos:
- Python 3.7+
- Flask 3.0.0
- Navegador moderno con JavaScript


PRÓXIMAS MEJORAS SUGERIDAS
==========================

- [ ] Editar compras después de realizadas
- [ ] Cancelar compras y liberar asientos
- [ ] Historial de asientos por usuario
- [ ] Notificación email con asientos
- [ ] Bloqueo de asientos durante selección
- [ ] Sugerencias de asientos cercanos
- [ ] Vista previa 3D del escenario
- [ ] Integración de pagos reales
- [ ] Multi-idioma
- [ ] Dashboard de vendedor


====================================================
Versión: 2.1
Fecha: 2026-05-24
Estado: ✅ Selección dinámica implementada
====================================================
