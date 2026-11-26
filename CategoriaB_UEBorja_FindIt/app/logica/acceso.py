"""Acceso del administrador. Las credenciales están en data/credenciales_demo.json.
Al cambiarlas desde Opciones, la contraseña se guarda cifrada (hash PBKDF2 con sal), nunca en texto."""
import hashlib
import json
import secrets

from app.datos import RUTA_CREDENCIALES, cargar_credenciales
from app.logica.validaciones import MIN_CLAVE


def _cifrar(clave, sal):
    return hashlib.pbkdf2_hmac("sha256", clave.encode(), bytes.fromhex(sal), 100_000).hex()


def _clave_correcta(credenciales, clave):
    if "sal" in credenciales:  # contraseña ya cifrada
        return _cifrar(clave, credenciales["sal"]) == credenciales["clave"]
    return clave == credenciales["clave"]  # credencial de demostración inicial


def verificar(usuario, clave):
    """Devuelve un mensaje de error, o None si el usuario y la clave son correctos."""
    if not usuario.strip() or not clave:
        return "Escribe el usuario y la contraseña."
    credenciales = cargar_credenciales()
    if usuario.strip() != credenciales["usuario"] or not _clave_correcta(credenciales, clave):
        return "Usuario o contraseña incorrectos."
    return None


def nombre_admin():
    return cargar_credenciales().get("nombre", "Administrador/a")


def cambiar_credenciales(clave_actual, nombre, usuario, nueva, confirmar):
    """Cambia nombre, usuario y contraseña. Por seguridad exige la contraseña actual y repetir la nueva."""
    credenciales = cargar_credenciales()
    if not _clave_correcta(credenciales, clave_actual):
        return "La contraseña actual no es correcta."
    if not usuario.strip() or not nombre.strip():
        return "Escribe tu nombre y tu usuario."
    if nueva or confirmar:
        if len(nueva) < MIN_CLAVE:
            return f"La contraseña nueva debe tener al menos {MIN_CLAVE} caracteres."
        if nueva != confirmar:
            return "Las contraseñas nuevas no coinciden."
        sal = secrets.token_hex(16)
        credenciales.update(sal=sal, clave=_cifrar(nueva, sal))
    credenciales.update(nombre=nombre.strip(), usuario=usuario.strip())
    credenciales["_nota"] = "Contraseña guardada cifrada (PBKDF2 + sal)."
    with open(RUTA_CREDENCIALES, "w", encoding="utf-8") as archivo:
        json.dump(credenciales, archivo, ensure_ascii=False, indent=2)
    return None
