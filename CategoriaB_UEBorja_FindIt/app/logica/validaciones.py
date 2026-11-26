"""Validaciones de formularios.

Devuelven un diccionario {campo: mensaje de error}. Si está vacío, todo está bien.
"""
import re
from datetime import date

MIN_TEXTO = 10  # Regla del reto: la seña particular debe tener al menos 10 caracteres

# Todos los niveles de un colegio en Ecuador: Inicial, Educación General Básica (EGB) y Bachillerato (BGU)
GRADOS = (["Inicial 1", "Inicial 2"]
          + [f"{n} EGB" for n in ("1ro", "2do", "3ro", "4to", "5to", "6to", "7mo", "8vo", "9no", "10mo")]
          + ["1ro BGU", "2do BGU", "3ro BGU", "Docente"])
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
PARALELOS = ["A", "B", "C", "D"]
CATEGORIAS = ["Ropa", "Útiles", "Tecnología", "Deportes", "Otros"]
DOCENTE = "Docente"


def _validar_nombre(valor, campo):
    """Nombre o apellido: obligatorio y solo letras y espacios."""
    valor = valor.strip()
    if not valor:
        return f"Escribe tu {campo}."
    if not all(letra.isalpha() or letra == " " for letra in valor):
        return f"El {campo} solo puede tener letras y espacios."
    return None


def validar_persona(nombre, apellido, grado, paralelo):
    """Datos de quien llena el formulario. Un docente no necesita paralelo."""
    errores = {}
    for campo, valor in (("nombre", nombre), ("apellido", apellido)):
        mensaje = _validar_nombre(valor, campo)
        if mensaje:
            errores[campo] = mensaje
    if grado not in GRADOS:
        errores["grado"] = "Selecciona tu grado."
    elif grado != DOCENTE and paralelo not in PARALELOS:
        errores["paralelo"] = "Selecciona tu paralelo."
    return errores


def validar_texto_largo(valor, campo, errores, nombre_visible):
    """Texto obligatorio con un mínimo de caracteres."""
    valor = valor.strip()
    if not valor:
        errores[campo] = f"Escribe {nombre_visible}."
    elif len(valor) < MIN_TEXTO:
        errores[campo] = f"Debe tener al menos {MIN_TEXTO} caracteres."


def validar_correo(correo, errores):
    """Correo obligatorio con formato válido (se recomienda el institucional)."""
    correo = correo.strip()
    if not correo:
        errores["correo"] = "Escribe tu correo (de preferencia el institucional)."
    elif not PATRON_CORREO.match(correo):
        errores["correo"] = "El correo no es válido. Ejemplo: nombre.apellido@colegio.edu.ec"


def validar_reclamo(nombre, apellido, correo, grado, paralelo, sena):
    errores = validar_persona(nombre, apellido, grado, paralelo)
    validar_correo(correo, errores)
    validar_texto_largo(sena, "sena", errores, "una seña particular del objeto")
    return errores


def validar_reporte(nombre, apellido, correo, grado, paralelo, objeto, categoria, lugar, descripcion):
    """Reporte de un objeto que alguien encontró y entregará en Inspección."""
    errores = validar_persona(nombre, apellido, grado, paralelo)
    validar_correo(correo, errores)
    if not objeto.strip():
        errores["objeto"] = "Escribe qué objeto encontraste."
    if categoria not in CATEGORIAS:
        errores["categoria"] = "Selecciona una categoría."
    if not lugar.strip():
        errores["lugar"] = "Escribe dónde lo encontraste."
    validar_texto_largo(descripcion, "descripcion", errores, "una descripción del objeto")
    return errores


def armar_curso(grado, paralelo):
    """Une grado y paralelo en un solo texto, ej. «2do BGU A». Un docente queda como «Docente»."""
    return grado if grado == DOCENTE else f"{grado} {paralelo}"


def validar_objeto(nombre, categoria, lugar, fecha, descripcion):
    """Objeto que registra el administrador. La fecha va como AAAA-MM-DD y no puede ser futura."""
    errores = {}
    if not nombre.strip():
        errores["nombre"] = "Escribe el nombre del objeto."
    if categoria not in CATEGORIAS:
        errores["categoria"] = "Selecciona una categoría."
    if not lugar.strip():
        errores["lugar"] = "Escribe dónde se encontró."
    try:
        if date.fromisoformat(fecha.strip()) > date.today():
            errores["fecha"] = "La fecha no puede ser futura."
    except ValueError:
        errores["fecha"] = "Usa el formato AAAA-MM-DD, por ejemplo 2026-11-26."
    validar_texto_largo(descripcion, "descripcion", errores, "una descripción del objeto")
    return errores
