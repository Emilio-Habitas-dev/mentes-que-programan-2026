"""Cuentas de estudiantes y profesores: registro e inicio de sesión.
La contraseña nunca se guarda tal cual: se guarda su «hash» (PBKDF2 con sal), de la librería estándar."""
import hashlib
import secrets

from app.datos import siguiente_id
from app.logica.validaciones import armar_curso, validar_registro


def _cifrar(clave, sal):
    return hashlib.pbkdf2_hmac("sha256", clave.encode(), bytes.fromhex(sal), 100_000).hex()


def buscar_por_correo(datos, correo):
    correo = correo.strip().lower()
    return next((u for u in datos["usuarios"] if u["correo"] == correo), None)


def buscar_por_id(datos, usuario_id):
    return next((u for u in datos["usuarios"] if u["id"] == usuario_id), None)


def registrar(datos, nombre, apellido, rol, grado, paralelo, correo, clave, confirmar):
    """Crea la cuenta. Devuelve (errores, usuario). El correo no se puede repetir."""
    errores = validar_registro(nombre, apellido, rol, grado, paralelo, correo, clave, confirmar)
    if "correo" not in errores and buscar_por_correo(datos, correo):
        errores["correo"] = "Ya existe una cuenta con ese correo. Inicia sesión."
    if errores:
        return errores, None
    sal = secrets.token_hex(16)
    usuario = {
        "id": siguiente_id(datos["usuarios"]),
        "nombre": nombre.strip(),
        "apellido": apellido.strip(),
        "rol": rol,
        "grado": grado,                                   # Profesor: grado en el que da clases
        "paralelo": paralelo if rol == "Estudiante" else "",
        "correo": correo.strip().lower(),
        "sal": sal,
        "clave": _cifrar(clave, sal),
    }
    datos["usuarios"].append(usuario)
    return {}, usuario


def iniciar_sesion(datos, correo, clave):
    """Devuelve (mensaje_de_error, usuario). El error no dice cuál dato falló (buena práctica)."""
    if not correo.strip() or not clave:
        return "Escribe tu correo y tu contraseña.", None
    usuario = buscar_por_correo(datos, correo)
    if not usuario or _cifrar(clave, usuario["sal"]) != usuario["clave"]:
        return "Correo o contraseña incorrectos.", None
    return None, usuario


def descripcion(usuario):
    """Texto corto para mostrar, ej. «Estudiante · 2do BGU A» o «Profesor · da clases en 5to EGB»."""
    if usuario["rol"] == "Profesor":
        return f"Profesor · da clases en {usuario['grado']}"
    return f"Estudiante · {armar_curso(usuario['grado'], usuario['paralelo'])}"


def datos_formulario(usuario):
    """Valores para llenar automáticamente los formularios de reclamo y reporte."""
    es_profesor = usuario["rol"] == "Profesor"
    return {"nombre": usuario["nombre"], "apellido": usuario["apellido"], "correo": usuario["correo"],
            "grado": "Docente" if es_profesor else usuario["grado"],
            "paralelo": "" if es_profesor else usuario["paralelo"]}
