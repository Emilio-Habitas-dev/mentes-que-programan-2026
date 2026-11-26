"""Reclamos. Aquí vive la regla principal del reto:
solo se puede reclamar un objeto Disponible y, al reclamarlo, pasa a Reclamado."""
from datetime import date

from app.datos import siguiente_id
from app.logica import objetos
from app.logica.validaciones import armar_curso, validar_reclamo

PENDIENTE = "Pendiente"


def puede_reclamar(objeto):
    """Usada por los botones «Reclamar» y por el registro: la misma regla en un solo lugar."""
    return objeto["estado"] == objetos.DISPONIBLE


def registrar_reclamo(datos, objeto_id, nombre, apellido, grado, paralelo, sena):
    """Valida y registra el reclamo. Devuelve (errores, reclamo_creado)."""
    errores = validar_reclamo(nombre, apellido, grado, paralelo, sena)
    objeto = objetos.buscar_por_id(datos, objeto_id)
    if not puede_reclamar(objeto):
        errores["general"] = f"Este objeto ya está {objeto['estado']}; no se puede reclamar."
    if errores:
        return errores, None

    reclamo = {
        "id": siguiente_id(datos["reclamos"]),
        "objeto_id": objeto_id,
        "nombre": nombre.strip(),
        "apellido": apellido.strip(),
        "curso": armar_curso(grado, paralelo),
        "sena": sena.strip(),
        "fecha": date.today().isoformat(),
        "estado": PENDIENTE,
    }
    datos["reclamos"].append(reclamo)
    objetos.cambiar_estado(objeto, objetos.RECLAMADO)  # Regla del reto: pasa a Reclamado
    return {}, reclamo


def pendientes(datos):
    """Reclamos que Inspección todavía no ha entregado ni rechazado."""
    return [r for r in datos["reclamos"] if r.get("estado", PENDIENTE) == PENDIENTE]


def _resolver(datos, reclamo_id, estado_objeto, estado_reclamo):
    """Cierra un reclamo y cambia el estado del objeto (si la transición es válida)."""
    reclamo = next(r for r in datos["reclamos"] if r["id"] == reclamo_id)
    error = objetos.cambiar_estado(objetos.buscar_por_id(datos, reclamo["objeto_id"]), estado_objeto)
    if not error:
        reclamo["estado"] = estado_reclamo
    return error


def entregar(datos, reclamo_id):
    """El dueño retiró el objeto: pasa a Entregado."""
    return _resolver(datos, reclamo_id, objetos.ENTREGADO, "Entregado")


def rechazar(datos, reclamo_id):
    """La seña no coincide: el objeto vuelve a Disponible."""
    return _resolver(datos, reclamo_id, objetos.DISPONIBLE, "Rechazado")
