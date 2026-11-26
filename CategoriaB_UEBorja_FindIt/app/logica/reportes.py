"""Reportes de objetos ENCONTRADOS: un estudiante o profesor avisa que encontró algo y lo lleva a Inspección.
Cuando Inspección recibe el objeto, el reporte se convierte automáticamente en un objeto Disponible del listado."""
from app.datos import siguiente_id
from app.logica import mensajes, objetos
from app.logica.validaciones import armar_curso, validar_reporte
from datetime import date

PENDIENTE = "Pendiente"
AGREGADO = "Agregado al listado"
DESCARTADO = "Descartado"


def registrar_reporte(datos, nombre, apellido, correo, grado, paralelo, objeto, categoria, lugar, descripcion,
                      usuario_id=None, foto=None):
    """Valida y guarda el reporte. foto: nombre del archivo ya guardado en data/fotos (opcional).
    Devuelve (errores, reporte_creado)."""
    errores = validar_reporte(nombre, apellido, correo, grado, paralelo, objeto, categoria, lugar, descripcion)
    if errores:
        return errores, None
    reporte = {
        "id": siguiente_id(datos["reportes"]),
        "nombre": nombre.strip(),
        "apellido": apellido.strip(),
        "correo": correo.strip().lower(),
        "curso": armar_curso(grado, paralelo),
        "objeto": objeto.strip(),
        "categoria": categoria,
        "lugar": lugar.strip(),
        "descripcion": descripcion.strip(),
        "fecha": date.today().isoformat(),
        "estado": PENDIENTE,
        "usuario_id": usuario_id,
        "foto": foto,
    }
    datos["reportes"].append(reporte)
    return {}, reporte


def pendientes(datos):
    return [r for r in datos["reportes"] if r["estado"] == PENDIENTE]


def _buscar(datos, reporte_id):
    return next(r for r in datos["reportes"] if r["id"] == reporte_id)


def agregar_al_listado(datos, reporte_id):
    """El administrador aprueba el reporte: se publica en el listado como Disponible y se avisa a quien lo encontró."""
    reporte = _buscar(datos, reporte_id)
    nuevo = objetos.crear_objeto(datos, reporte["objeto"], reporte["categoria"], reporte["lugar"],
                                 reporte["fecha"], reporte["descripcion"], reporte.get("foto"),
                                 reporte.get("usuario_id"))
    mensajes.enviar(datos, reporte.get("usuario_id"), "Tu reporte fue publicado",
                    f"«{reporte['objeto']}» ya aparece en el listado. Guárdalo hasta que te avisemos: "
                    "cuando aparezca el dueño te diremos la hora de entrega.")
    reporte["estado"] = AGREGADO
    reporte["objeto_id"] = nuevo["id"]
    return nuevo


def descartar(datos, reporte_id):
    """El objeto nunca llegó a Inspección (o el reporte era un error)."""
    _buscar(datos, reporte_id)["estado"] = DESCARTADO
