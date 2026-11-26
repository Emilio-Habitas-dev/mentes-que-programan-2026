"""Cuentas de estudiantes y profesores: registro e inicio de sesión.
La contraseña nunca se guarda tal cual: se guarda su «hash» (PBKDF2 con sal), de la librería estándar."""
import hashlib
import secrets
from datetime import datetime

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
        "registrado": datetime.now().strftime("%Y-%m-%d %H:%M"),
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


def cambiar_clave(usuario, nueva, confirmar):
    """Pone una contraseña nueva (cifrada). Devuelve un mensaje de error o None."""
    from app.logica.validaciones import MIN_CLAVE
    if len(nueva) < MIN_CLAVE:
        return f"La contraseña debe tener al menos {MIN_CLAVE} caracteres."
    if nueva != confirmar:
        return "Las contraseñas no coinciden."
    usuario["sal"] = secrets.token_hex(16)
    usuario["clave"] = _cifrar(nueva, usuario["sal"])
    return None


def editar(datos, usuario_id, nombre, apellido, correo, nueva_clave="", confirmar=""):
    """El administrador corrige los datos de una cuenta y, si quiere, le pone una contraseña nueva."""
    from app.logica.validaciones import PATRON_CORREO, _validar_nombre
    usuario = buscar_por_id(datos, usuario_id)
    for campo, valor in (("nombre", nombre), ("apellido", apellido)):
        error = _validar_nombre(valor, campo)
        if error:
            return error
    correo = correo.strip().lower()
    if not PATRON_CORREO.match(correo):
        return "El correo no es válido."
    otro = buscar_por_correo(datos, correo)
    if otro and otro["id"] != usuario_id:
        return "Ya existe otra cuenta con ese correo."
    if nueva_clave:
        error = cambiar_clave(usuario, nueva_clave, confirmar)
        if error:
            return error
    usuario.update(nombre=nombre.strip(), apellido=apellido.strip(), correo=correo)
    return None


def borrar(datos, usuario_id):
    """Elimina la cuenta y sus mensajes (sus reclamos y reportes quedan como historial)."""
    datos["usuarios"] = [u for u in datos["usuarios"] if u["id"] != usuario_id]
    datos["mensajes"] = [m for m in datos["mensajes"] if m["usuario_id"] != usuario_id]
