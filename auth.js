// Verificar si el usuario inició sesión
if (localStorage.getItem('auth_authenticated') !== 'true') {
    window.location.href = 'login.html';
}

// Función para cerrar sesión globalmente
function cerrarSesion() {
    localStorage.removeItem('auth_authenticated');
    window.location.href = 'login.html';
}