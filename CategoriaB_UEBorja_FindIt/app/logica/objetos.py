"""Reglas de los objetos: búsqueda, filtros, conteo y cambios de estado válidos."""
from datetime import date

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
