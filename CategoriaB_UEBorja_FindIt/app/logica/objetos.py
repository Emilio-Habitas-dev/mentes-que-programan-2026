"""Reglas de los objetos: búsqueda, filtros, conteo y cambios de estado válidos."""
from datetime import date

from app.datos import siguiente_id
from app.logica.validaciones import validar_objeto

DISPONIBLE = "Disponible"
RECLAMADO = "Reclamado"
ENTREGADO = "Entregado"
ESTADOS = [DISPONIBLE, RECLAMADO, ENTREGADO]
TODAS = "Todas"
TODOS = "Todos"

# Cambios de estado permitidos. Toda la app pasa por aquí, así ningún objeto queda en un estado imposible.
#   Disponible -> Reclamado   (alguien registra un reclamo)
#   Reclamado  -> Entregado   (Inspección lo entrega a su dueño)
#   Reclamado  -> Disponible  (Inspección rechaza el reclamo)
TRANSICIONES = {DISPONIBLE: [RECLAMADO], RECLAMADO: [ENTREGADO, DISPONIBLE], ENTREGADO: []}


def buscar_por_id(datos, objeto_id):
    """Devuelve el objeto con ese id, o None si no existe."""
    for objeto in datos["objetos"]:
        if objeto["id"] == objeto_id:
            return objeto
    return None


def categorias(datos):
    """Categorías sin repetir, en orden alfabético."""
    return sorted({objeto["categoria"] for objeto in datos["objetos"]})


def filtrar(datos, texto, categoria, estado):
    """Objetos que coinciden con el texto (nombre, lugar o descripción), la categoría y el estado."""
    texto = texto.lower().strip()
    resultado = []
    for objeto in datos["objetos"]:
        donde_buscar = f"{objeto['nombre']} {objeto['lugar']} {objeto['descripcion']}".lower()
        if texto and texto not in donde_buscar:
            continue
        if categoria != TODAS and objeto["categoria"] != categoria:
            continue
        if estado != TODOS and objeto["estado"] != estado:
            continue
        resultado.append(objeto)
    return resultado


def describir_filtros(texto, categoria, estado):
    """Texto con los filtros activos, para explicar por qué no hay resultados."""
    partes = []
    if texto.strip():
        partes.append(f"búsqueda «{texto.strip()}»")
    if categoria != TODAS:
        partes.append(f"categoría {categoria}")
    if estado != TODOS:
        partes.append(f"estado {estado}")
    return " + ".join(partes)


def contar_por_estado(datos):
    """Conteo para las tarjetas de resumen: Total y uno por cada estado."""
    conteo = {"Total": len(datos["objetos"])}
    for estado in ESTADOS:
        conteo[estado] = sum(1 for objeto in datos["objetos"] if objeto["estado"] == estado)
    return conteo


def cambiar_estado(objeto, nuevo_estado):
    """Cambia el estado solo si la transición está permitida. Devuelve un mensaje de error o None."""
    if nuevo_estado not in TRANSICIONES.get(objeto["estado"], []):
        return f"No se puede pasar de {objeto['estado']} a {nuevo_estado}."
    objeto["estado"] = nuevo_estado
    objeto["fecha_entrega"] = date.today().isoformat() if nuevo_estado == ENTREGADO else None
    return None


def crear_objeto(datos, nombre, categoria, lugar, fecha, descripcion):
    """Agrega un objeto nuevo al listado. Siempre empieza Disponible."""
    objeto = {
        "id": siguiente_id(datos["objetos"]),
        "nombre": nombre.strip(),
        "categoria": categoria,
        "lugar": lugar.strip(),
        "fecha_hallazgo": fecha.strip(),
        "estado": DISPONIBLE,
        "descripcion": descripcion.strip(),
        "fecha_entrega": None,
    }
    datos["objetos"].append(objeto)
    return objeto


def registrar_objeto(datos, nombre, categoria, lugar, fecha, descripcion):
    """Valida y registra un objeto desde el administrador. Devuelve (errores, objeto_creado)."""
    errores = validar_objeto(nombre, categoria, lugar, fecha, descripcion)
    if errores:
        return errores, None
    return {}, crear_objeto(datos, nombre, categoria, lugar, fecha, descripcion)


def borrar_objeto(datos, objeto_id):
    """Quita un objeto del listado. No se permite si tiene un reclamo pendiente (primero hay que resolverlo)."""
    pendiente = any(r["objeto_id"] == objeto_id and r.get("estado", "Pendiente") == "Pendiente"
                    for r in datos["reclamos"])
    if pendiente:
        return "Este objeto tiene un reclamo pendiente: entrégalo o recházalo antes de borrarlo."
    datos["objetos"] = [o for o in datos["objetos"] if o["id"] != objeto_id]
    return None
