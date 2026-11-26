"""Acceso del administrador con credenciales FICTICIAS de demostración (no es seguridad real)."""
from app.datos import cargar_credenciales


def verificar(usuario, clave):
    """Devuelve un mensaje de error, o None si el usuario y la clave son correctos."""
    if not usuario.strip() or not clave:
        return "Escribe el usuario y la contraseña."
    credenciales = cargar_credenciales()
    if usuario.strip() != credenciales["usuario"] or clave != credenciales["clave"]:
        return "Usuario o contraseña incorrectos."
    return None
