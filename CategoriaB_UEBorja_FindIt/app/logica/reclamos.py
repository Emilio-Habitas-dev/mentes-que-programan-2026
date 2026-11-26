"""Reclamos. Aquí vive la regla principal del reto:
solo se puede reclamar un objeto Disponible y, al reclamarlo, pasa a Reclamado.

Ciclo de un reclamo:  Pendiente -> Coordinado (el administrador fija la hora de entrega) -> Entregado
                      Pendiente o Coordinado -> Rechazado (el objeto vuelve a Disponible)"""
from datetime import date

from app.datos import siguiente_id
from app.logica import mensajes, objetos
from app.logica.validaciones import armar_curso, validar_hora, validar_reclamo

PENDIENTE = "Pendiente"
COORDINADO = "Coordinado"
ABIERTOS = (PENDIENTE, COORDINADO)  # Reclamos que aún no se cierran


def puede_reclamar(objeto):
    """Usada por los botones «Reclamar» y por el registro: la misma regla en un solo lugar."""
    return objeto["estado"] == objetos.DISPONIBLE


def registrar_reclamo(datos, objeto_id, nombre, apellido, correo, grado, paralelo, sena, usuario_id=None):
    """Valida y registra el reclamo. Devuelve (errores, reclamo_creado)."""
    errores = validar_reclamo(nombre, apellido, correo, grado, paralelo, sena)
    objeto = objetos.buscar_por_id(datos, objeto_id)
    if not puede_reclamar(objeto):
        errores["general"] = f"Este objeto ya está {objeto['estado']}; no se puede reclamar."
    if errores:
        return errores, None

    reclamo = {
        "id": siguiente_id(datos["reclamos"]),
        "objeto_id": objeto_id,
        "usuario_id": usuario_id,
        "nombre": nombre.strip(),
        "apellido": apellido.strip(),
        "correo": correo.strip().lower(),
        "curso": armar_curso(grado, paralelo),
        "sena": sena.strip(),
        "fecha": date.today().isoformat(),
        "estado": PENDIENTE,
        "hora_entrega": None,
    }
    datos["reclamos"].append(reclamo)
    objetos.cambiar_estado(objeto, objetos.RECLAMADO)  # Regla del reto: pasa a Reclamado
    return {}, reclamo


def pendientes(datos):
    """Reclamos abiertos (pendientes o con entrega coordinada) que ve el administrador."""
    return [r for r in datos["reclamos"] if r.get("estado", PENDIENTE) in ABIERTOS]


def _buscar(datos, reclamo_id):
    return next(r for r in datos["reclamos"] if r["id"] == reclamo_id)


def coordinar_entrega(datos, reclamo_id, fecha, hora, lugar=""):
    """El administrador acepta el reclamo y fija fecha, hora y lugar (por defecto el edificio administrativo).
    Avisa por mensaje al dueño y a quien encontró el objeto. Devuelve un mensaje de error o None."""
    try:
        dia = date.fromisoformat(fecha.strip())
    except ValueError:
        return "Escribe la fecha en formato AAAA-MM-DD (por ejemplo 2026-11-27)."
    if dia < date.today():
        return "La fecha de entrega no puede ser pasada."
    if not validar_hora(hora):
        return "Escribe la hora en formato HH:MM (por ejemplo 13:30)."
    lugar = lugar.strip() or mensajes.LUGAR_ENTREGA
    reclamo = _buscar(datos, reclamo_id)
    objeto = objetos.buscar_por_id(datos, reclamo["objeto_id"])
    reclamo.update(estado=COORDINADO, fecha_cita=dia.isoformat(), hora_entrega=hora.strip(), lugar_entrega=lugar)
    cita = f"{lugar} el {dia.strftime('%d/%m/%Y')} a las {hora.strip()}"
    mensajes.enviar(datos, reclamo.get("usuario_id"), "Tu reclamo fue aprobado",
                    f"¡Listo! Tu reclamo de «{objeto['nombre']}» fue aprobado. Retíralo en {cita}. "
                    "Al retirarlo te pediremos describir la seña particular del objeto para confirmar que es tuyo.")
    mensajes.enviar(datos, objeto.get("reportado_por"), "¡Encontramos al dueño!",
                    f"¡Listo, encontramos al dueño de «{objeto['nombre']}»! Entrégalo en {cita}. "
                    "Gracias por ayudar.")
    return None


def entregar(datos, reclamo_id):
    """El dueño retiró el objeto: pasa a Entregado."""
    reclamo = _buscar(datos, reclamo_id)
    error = objetos.cambiar_estado(objetos.buscar_por_id(datos, reclamo["objeto_id"]), objetos.ENTREGADO)
    if not error:
        reclamo["estado"] = "Entregado"
    return error


def rechazar(datos, reclamo_id):
    """La seña no coincide: el objeto vuelve a Disponible y se avisa a quien reclamó."""
    reclamo = _buscar(datos, reclamo_id)
    objeto = objetos.buscar_por_id(datos, reclamo["objeto_id"])
    error = objetos.cambiar_estado(objeto, objetos.DISPONIBLE)
    if not error:
        reclamo["estado"] = "Rechazado"
        mensajes.enviar(datos, reclamo.get("usuario_id"), "Reclamo rechazado",
                        f"Tu reclamo de «{objeto['nombre']}» no fue aprobado: la seña particular no coincide. "
                        "Si crees que es un error, acércate al edificio administrativo.")
    return error
