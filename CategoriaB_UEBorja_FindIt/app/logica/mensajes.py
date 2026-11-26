"""Buzón de mensajes de cada usuario (ícono ✉ en la barra superior)."""
from datetime import datetime

from app.datos import siguiente_id

LUGAR_ENTREGA = "el edificio administrativo del colegio"


def enviar(datos, usuario_id, titulo, texto):
    """Deja un mensaje en el buzón del usuario. Si no hay usuario (datos antiguos), no hace nada."""
    if usuario_id is None:
        return
    datos["mensajes"].append({
        "id": siguiente_id(datos["mensajes"]),
        "usuario_id": usuario_id,
        "titulo": titulo,
        "texto": texto,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "leido": False,
    })


def de_usuario(datos, usuario_id):
    """Mensajes del usuario, el más reciente primero."""
    return sorted((m for m in datos["mensajes"] if m["usuario_id"] == usuario_id),
                  key=lambda m: m["id"], reverse=True)


def no_leidos(datos, usuario_id):
    return sum(1 for m in de_usuario(datos, usuario_id) if not m["leido"])


def marcar_leido(datos, mensaje_id):
    next(m for m in datos["mensajes"] if m["id"] == mensaje_id)["leido"] = True
