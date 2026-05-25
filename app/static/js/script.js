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
    
    // Actualizar total en tiempo real
    const cantidadInput = document.getElementById('cantidad');
    if (cantidadInput) {
        cantidadInput.addEventListener('change', function() {
            const nuevaCantidad = parseInt(this.value);
            if (nuevaCantidad <= 0) {
                this.value = 1;
            }
        });
    }
    
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
