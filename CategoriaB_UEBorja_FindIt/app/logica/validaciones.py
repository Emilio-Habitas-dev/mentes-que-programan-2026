"""Validaciones de formularios.

Devuelven un diccionario {campo: mensaje de error}. Si está vacío, todo está bien.
"""
MIN_TEXTO = 10  # Regla del reto: la seña particular debe tener al menos 10 caracteres

GRADOS = ["8vo EGB", "9no EGB", "10mo EGB", "1ro BGU", "2do BGU", "3ro BGU", "Docente"]
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


def validar_reclamo(nombre, apellido, grado, paralelo, sena):
    errores = validar_persona(nombre, apellido, grado, paralelo)
    validar_texto_largo(sena, "sena", errores, "una seña particular del objeto")
    return errores


def validar_reporte(nombre, apellido, grado, paralelo, objeto, categoria, lugar, descripcion):
    errores = validar_persona(nombre, apellido, grado, paralelo)
    if not objeto.strip():
        errores["objeto"] = "Escribe qué objeto perdiste."
    if categoria not in CATEGORIAS:
        errores["categoria"] = "Selecciona una categoría."
    if not lugar.strip():
        errores["lugar"] = "Escribe dónde lo perdiste."
    validar_texto_largo(descripcion, "descripcion", errores, "una descripción del objeto")
    return errores


def armar_curso(grado, paralelo):
    """Une grado y paralelo en un solo texto, ej. «2do BGU A». Un docente queda como «Docente»."""
    return grado if grado == DOCENTE else f"{grado} {paralelo}"
