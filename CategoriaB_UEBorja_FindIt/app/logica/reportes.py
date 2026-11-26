"""Reportes de objetos perdidos que envían estudiantes o profesores para que Inspección los busque."""
from datetime import date

from app.datos import siguiente_id
from app.logica.validaciones import armar_curso, validar_reporte

PENDIENTE = "Pendiente"


def registrar_reporte(datos, nombre, apellido, grado, paralelo, objeto, categoria, lugar, descripcion):
    """Valida y guarda el reporte. Devuelve (errores, reporte_creado)."""
    errores = validar_reporte(nombre, apellido, grado, paralelo, objeto, categoria, lugar, descripcion)
    if errores:
        return errores, None
    reporte = {
        "id": siguiente_id(datos["reportes"]),
        "nombre": nombre.strip(),
        "apellido": apellido.strip(),
        "curso": armar_curso(grado, paralelo),
        "objeto": objeto.strip(),
        "categoria": categoria,
        "lugar": lugar.strip(),
        "descripcion": descripcion.strip(),
        "fecha": date.today().isoformat(),
        "estado": PENDIENTE,
    }
    datos["reportes"].append(reporte)
    return {}, reporte


def pendientes(datos):
    return [r for r in datos["reportes"] if r["estado"] == PENDIENTE]


def marcar_atendido(datos, reporte_id):
    """Inspección ya revisó el reporte."""
    next(r for r in datos["reportes"] if r["id"] == reporte_id)["estado"] = "Atendido"
