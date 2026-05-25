// Script para mejorar UX

document.addEventListener('DOMContentLoaded', function() {
    // Validación de formulario en tiempo real
    const formCompra = document.getElementById('formCompra');
    if (formCompra) {
        formCompra.addEventListener('submit', function(e) {
            const nombre = document.getElementById('nombre').value.trim();
            const correo = document.getElementById('correo').value.trim();
            const cantidad = parseInt(document.getElementById('cantidad').value);
            
            if (!nombre || !correo || cantidad <= 0) {
                e.preventDefault();
                alert('Por favor completa todos los campos correctamente');
                return false;
            }
        });
    }
    
    // Actualización de cantidad (REMOVIDO - incompatible con v2.1.1 que usa selección de asientos)
    // El código de actualizarResumen() en comprar.html maneja la actualización correctamente
    
    // Animación de carga de imágenes
    const imagenes = document.querySelectorAll('img');
    imagenes.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.3s ease';
    });
    
    // Tooltip de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Interactividad del mapa de asientos (REMOVIDO - conflictúa con toggleAsiento() en comprar.html)
    // El código de toggleAsiento() en comprar.html maneja la selección de asientos correctamente
    // incluyendo deselección, validación de ocupados, etc.
});

// Función para formatear dinero
function formatearDinero(cantidad) {
    return '$' + parseFloat(cantidad).toFixed(2);
}

// Función para mostrar notificación
function mostrarNotificacion(mensaje, tipo = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${tipo} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const mainContent = document.querySelector('main');
    mainContent.insertBefore(alertDiv, mainContent.firstChild);
    
    // Auto cerrar después de 5 segundos
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Función para actualizar asientos seleccionados
function actualizarAsientosSeleccionados() {
    const seleccionados = document.querySelectorAll('.asiento.seleccionado');
    const cantidad = seleccionados.length;
    
    if (cantidad > 0) {
        console.log(`Asientos seleccionados: ${cantidad}`);
    }
}

// Función para cargar mapa de asientos vía API
async function cargarMapaAsientos(evento_id) {
    try {
        const response = await fetch(`/api/asientos/${evento_id}`);
        const data = await response.json();
        
        console.log(`Total: ${data.total_asientos}, Disponibles: ${data.disponibles}, Ocupados: ${data.ocupados}`);
        
        return data;
    } catch (error) {
        console.error('Error al cargar mapa de asientos:', error);
        mostrarNotificacion('Error al cargar el mapa de asientos', 'danger');
    }
}

// Función para descargar PDF con confirmación visual
function descargarPDF(compra_id, nombre_evento) {
    mostrarNotificacion(`📥 Descargando entrada para ${nombre_evento}...`, 'info');
    
    setTimeout(() => {
        window.location.href = `/descargar-entrada/${compra_id}`;
    }, 500);
}
