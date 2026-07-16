/*
 * Ejercicio 3 - Pruebas de Rendimiento utilizando k6
 * API: Plataforma de Venta de Entradas para Eventos (Flask)
 *      https://github.com/DanLAQP/Plataforma-de-venta-de-entradas-para-eventos
 *      La API corre en http://localhost:5000 y expone recursos REST bajo /api.
 *
 * El escenario (VUs y duracion) se parametriza por variables de entorno para
 * ejecutar las 3 configuraciones minimas exigidas por la guia:
 *
 *   Escenario A:  VUS=20   DURATION=30s
 *   Escenario B:  VUS=50   DURATION=45s
 *   Escenario C:  VUS=100  DURATION=60s
 *
 * Ejecucion (ejemplo escenario A):
 *   k6 run -e VUS=20 -e DURATION=30s prueba_ejercicio3.js
 *
 * Cada iteracion ejerce tres endpoints de solo-lectura (GET): la lista de
 * eventos, el detalle de un evento y su mapa de asientos. Se usan operaciones
 * de lectura para mantener el estado (archivos JSON) estable durante la prueba
 * y que la comparacion con Apache JMeter sea sobre el mismo tipo de operacion.
 * Al terminar, k6 imprime en consola el resumen con todas las metricas.
 */
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE = __ENV.BASE || 'http://localhost:5000';
const VUS = parseInt(__ENV.VUS || '20', 10);
const DURATION = __ENV.DURATION || '30s';

const EVENTO_ID = __ENV.EVENTO_ID || '1';

export const options = {
  vus: VUS,
  duration: DURATION,
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const eventos = http.get(`${BASE}/api/eventos`);
  check(eventos, {
    'GET /api/eventos status 200': (r) => r.status === 200,
    'GET /api/eventos devuelve arreglo': (r) => Array.isArray(r.json()),
  });

  const detalle = http.get(`${BASE}/api/eventos/${EVENTO_ID}`);
  check(detalle, {
    'GET /api/eventos/:id status 200': (r) => r.status === 200,
  });

  const asientos = http.get(`${BASE}/api/eventos/${EVENTO_ID}/asientos`);
  check(asientos, {
    'GET /api/eventos/:id/asientos status 200': (r) => r.status === 200,
    'asientos trae 150 butacas': (r) => (r.json('total_asientos') === 150),
  });

  sleep(1);
}
