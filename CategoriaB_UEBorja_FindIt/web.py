"""FIND IT - versión WEB (Flask). Usa exactamente la misma lógica y los mismos datos que la versión de escritorio:
solo cambia la interfaz (páginas HTML en templates/ en lugar de ventanas Tkinter).

Ejecutar:  python web.py      ->  abrir http://localhost:5000
Otros equipos de la misma red:  http://<IP-de-este-equipo>:5000
"""
import secrets
from functools import wraps
from pathlib import Path

from flask import Flask, abort, jsonify, redirect, render_template, request, send_from_directory, session, url_for

from app import datos as almacen
from app.logica import acceso, mensajes, objetos, reclamos, reportes, usuarios
from app.logica.validaciones import CATEGORIAS, GRADOS, PARALELOS, ROLES

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # clave de sesión aleatoria en cada arranque (no se guarda en el código)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # fotos de hasta 5 MB
FORMATOS_WEB = (".png", ".gif", ".jpg", ".jpeg", ".webp")
GRADOS_CUENTA = [g for g in GRADOS if g != "Docente"]


# ---------- Ayudantes ----------

def usuario_actual(datos):
    return usuarios.buscar_por_id(datos, session.get("usuario_id")) if session.get("usuario_id") else None


@app.context_processor
def datos_para_plantillas():
    """Variables disponibles en todas las páginas: quién está conectado y cuántos mensajes sin leer tiene."""
    datos = almacen.cargar()
    usuario = usuario_actual(datos)
    return {"usuario": usuario, "es_admin": session.get("admin", False),
            "descripcion_usuario": usuarios.descripcion(usuario) if usuario else "",
            "no_leidos": mensajes.no_leidos(datos, usuario["id"]) if usuario else 0}


def requiere_usuario(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("usuario_id") and not session.get("admin"):
            return redirect(url_for("acceso_vista"))
        return vista(*args, **kwargs)
    return envoltura


def requiere_admin(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return vista(*args, **kwargs)
    return envoltura


def confirmacion(exito, titulo, detalle, objeto_id=None):
    return render_template("confirmacion.html", exito=exito, titulo=titulo, detalle=detalle, objeto_id=objeto_id)


# ---------- Inicio y cuentas ----------

@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/acceso", methods=["GET", "POST"])
def acceso_vista():
    datos = almacen.cargar()
    contexto = {"roles": ROLES, "grados": GRADOS_CUENTA, "paralelos": PARALELOS, "errores": {}, "valores": {},
                "error_login": ""}
    if request.method == "POST" and request.form.get("accion") == "login":
        error, usuario = usuarios.iniciar_sesion(datos, request.form.get("correo", ""), request.form.get("clave", ""))
        if not error:
            session.clear()
            session["usuario_id"] = usuario["id"]
            return redirect(url_for("listado"))
        contexto["error_login"] = error
    elif request.method == "POST":
        valores = {c: request.form.get(c, "") for c in
                   ("nombre", "apellido", "rol", "grado", "grado_clase", "paralelo", "correo", "clave", "confirmar")}
        es_profesor = valores["rol"] == "Profesor"
        envio = {k: v for k, v in valores.items() if k != "grado_clase"}
        if es_profesor:
            envio["grado"], envio["paralelo"] = valores["grado_clase"], ""
        errores, usuario = usuarios.registrar(datos, **envio)
        if not errores:
            almacen.guardar(datos)
            session.clear()
            session["usuario_id"] = usuario["id"]
            return redirect(url_for("listado"))
        if es_profesor and "grado" in errores:
            errores["grado_clase"] = errores.pop("grado")
        contexto.update(errores=errores, valores=valores)
    return render_template("acceso.html", **contexto)


@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("inicio"))


# ---------- Objetos ----------

@app.route("/listado")
@requiere_usuario
def listado():
    datos = almacen.cargar()
    texto = request.args.get("q", "")
    categoria = request.args.get("categoria", objetos.TODAS)
    estado = request.args.get("estado", objetos.TODOS)
    encontrados = objetos.filtrar(datos, texto, categoria, estado)
    return render_template("listado.html", objetos_lista=encontrados, conteo=objetos.contar_por_estado(datos),
                           categorias=objetos.categorias(datos), estados=objetos.ESTADOS, q=texto,
                           categoria=categoria, estado=estado, puede_reclamar=reclamos.puede_reclamar,
                           filtros=objetos.describir_filtros(texto, categoria, estado))


@app.route("/objeto/<int:objeto_id>")
@requiere_usuario
def detalle(objeto_id):
    objeto = objetos.buscar_por_id(almacen.cargar(), objeto_id) or abort(404)
    return render_template("detalle.html", objeto=objeto, se_puede=reclamos.puede_reclamar(objeto), error="")


@app.route("/objeto/<int:objeto_id>/borrar", methods=["POST"])
@requiere_admin
def borrar(objeto_id):
    datos = almacen.cargar()
    error = objetos.borrar_objeto(datos, objeto_id)
    if error:
        objeto = objetos.buscar_por_id(datos, objeto_id)
        return render_template("detalle.html", objeto=objeto, se_puede=False, error=error)
    almacen.guardar(datos)
    return redirect(url_for("listado"))


@app.route("/objeto/<int:objeto_id>/reclamar", methods=["GET", "POST"])
@requiere_usuario
def reclamar(objeto_id):
    datos = almacen.cargar()
    if session.get("admin"):
        return redirect(url_for("detalle", objeto_id=objeto_id))  # el administrador no reclama
    objeto = objetos.buscar_por_id(datos, objeto_id) or abort(404)
    usuario = usuario_actual(datos)
    valores = usuarios.datos_formulario(usuario) | {"sena": ""}
    errores = {}
    if request.method == "POST":
        valores = {c: request.form.get(c, "") for c in ("nombre", "apellido", "correo", "grado", "paralelo", "sena")}
        errores, _ = reclamos.registrar_reclamo(datos, objeto_id, **valores, usuario_id=usuario["id"])
        if "general" in errores:
            return confirmacion(False, "No se pudo registrar el reclamo", errores["general"], objeto_id)
        if not errores:
            almacen.guardar(datos)
            return confirmacion(True, "¡Reclamo registrado!",
                                f"El objeto «{objeto['nombre']}» ahora está Reclamado. Te avisaremos en ✉ "
                                "la hora de entrega en el edificio administrativo.")
    return render_template("reclamo.html", objeto=objeto, valores=valores, errores=errores,
                           grados=GRADOS, paralelos=PARALELOS)


@app.route("/reportar", methods=["GET", "POST"])
@requiere_usuario
def reportar():
    datos = almacen.cargar()
    usuario = usuario_actual(datos)
    if not usuario:
        return redirect(url_for("listado"))
    valores = usuarios.datos_formulario(usuario) | {"objeto": "", "categoria": "", "lugar": "", "descripcion": ""}
    errores = {}
    if request.method == "POST":
        valores = {c: request.form.get(c, "") for c in
                   ("nombre", "apellido", "correo", "grado", "paralelo", "objeto", "categoria", "lugar", "descripcion")}
        foto = request.files.get("foto")
        extension = Path(foto.filename).suffix.lower() if foto and foto.filename else ""
        if extension and extension not in FORMATOS_WEB:
            errores["foto"] = "La foto debe ser PNG, JPG, GIF o WEBP."
        else:
            errores, reporte = reportes.registrar_reporte(datos, **valores, usuario_id=usuario["id"])
            if not errores:
                if extension:  # guardar la foto en data/fotos con el número del reporte
                    almacen.CARPETA_FOTOS.mkdir(exist_ok=True)
                    nombre = f"reporte_{reporte['id']}{extension}"
                    foto.save(almacen.CARPETA_FOTOS / nombre)
                    reporte["foto"] = nombre
                almacen.guardar(datos)
                return confirmacion(True, "¡Gracias por reportarlo!",
                                    f"El administrador revisará tu reporte de «{reporte['objeto']}». Guárdalo: "
                                    "te avisaremos en ✉ cuando aparezca el dueño y la hora de entrega.")
    return render_template("reportar.html", valores=valores, errores=errores, grados=GRADOS,
                           paralelos=PARALELOS, categorias=CATEGORIAS)


@app.route("/api/notificaciones")
def notificaciones():
    """Números que la página consulta cada pocos segundos para actualizar ✉ y los contadores del panel."""
    datos = almacen.cargar()
    usuario = usuario_actual(datos)
    return jsonify(no_leidos=mensajes.no_leidos(datos, usuario["id"]) if usuario else 0,
                   solicitudes=len(reclamos.pendientes(datos)), reportes=len(reportes.pendientes(datos)))


@app.route("/foto/<nombre>")
def foto(nombre):
    return send_from_directory(almacen.CARPETA_FOTOS, nombre)


# ---------- Buzón ----------

@app.route("/buzon")
@app.route("/buzon/<int:mensaje_id>")
@requiere_usuario
def buzon(mensaje_id=None):
    datos = almacen.cargar()
    usuario = usuario_actual(datos)
    if not usuario:
        return redirect(url_for("listado"))
    abierto = None
    if mensaje_id:
        abierto = next((m for m in mensajes.de_usuario(datos, usuario["id"]) if m["id"] == mensaje_id), None)
        if abierto and not abierto["leido"]:
            mensajes.marcar_leido(datos, mensaje_id)
            almacen.guardar(datos)
    return render_template("buzon.html", lista=mensajes.de_usuario(datos, usuario["id"]), abierto=abierto)


# ---------- Administrador ----------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = ""
    if request.method == "POST":
        error = acceso.verificar(request.form.get("usuario", ""), request.form.get("clave", ""))
        if not error:
            session.clear()
            session["admin"] = True
            return redirect(url_for("panel"))
    return render_template("admin_login.html", error=error)  # noqa


@app.route("/admin")
@requiere_admin
def panel():
    datos = almacen.cargar()
    return render_template("panel.html", solicitudes=len(reclamos.pendientes(datos)), cuentas=len(datos["usuarios"]),
                           nombre_admin=acceso.nombre_admin(),
                           reportes_pendientes=len(reportes.pendientes(datos)))


@app.route("/admin/solicitudes", methods=["GET", "POST"])
@requiere_admin
def solicitudes():
    datos = almacen.cargar()
    aviso, error = "", False
    if request.method == "POST":
        reclamo_id = int(request.form["reclamo_id"])
        accion = request.form["accion"]
        if accion == "coordinar":
            resultado = reclamos.coordinar_entrega(datos, reclamo_id, request.form.get("fecha", ""),
                                                   request.form.get("hora", ""), request.form.get("lugar", ""))
            aviso = resultado or "Entrega coordinada. Se enviaron los mensajes al dueño y a quien lo encontró."
        elif accion == "entregar":
            resultado = reclamos.entregar(datos, reclamo_id)
            aviso = resultado or "Objeto marcado como Entregado."
        else:
            resultado = reclamos.rechazar(datos, reclamo_id)
            aviso = resultado or "Reclamo rechazado. El objeto volvió a Disponible."
        error = bool(resultado)
        if not error:
            almacen.guardar(datos)
    filas = [(r, objetos.buscar_por_id(datos, r["objeto_id"])) for r in reclamos.pendientes(datos)]
    from datetime import date
    return render_template("solicitudes.html", filas=filas, aviso=aviso, error=error, coordinado=reclamos.COORDINADO,
                           hoy=date.today().isoformat(), lugar=mensajes.LUGAR_ENTREGA)


@app.route("/admin/reportes", methods=["GET", "POST"])
@requiere_admin
def admin_reportes():
    datos = almacen.cargar()
    aviso = ""
    if request.method == "POST":
        reporte_id = int(request.form["reporte_id"])
        if request.form["accion"] == "publicar":
            nuevo = reportes.agregar_al_listado(datos, reporte_id)
            aviso = f"«{nuevo['nombre']}» publicado en el listado (ID {nuevo['id']:02d})."
        else:
            reportes.descartar(datos, reporte_id)
            aviso = "Reporte descartado."
        almacen.guardar(datos)
    return render_template("admin_reportes.html", lista=reportes.pendientes(datos), aviso=aviso)


@app.route("/admin/registrar", methods=["GET", "POST"])
@requiere_admin
def registrar_objeto():
    from datetime import date
    datos = almacen.cargar()
    valores = {"nombre": "", "categoria": "", "lugar": "", "fecha": date.today().isoformat(), "descripcion": ""}
    errores = {}
    if request.method == "POST":
        valores = {c: request.form.get(c, "") for c in valores}
        errores, objeto = objetos.registrar_objeto(datos, **valores)
        if not errores:
            almacen.guardar(datos)
            return confirmacion(True, "¡Objeto registrado!",
                                f"«{objeto['nombre']}» ya está en el listado como Disponible (ID {objeto['id']:02d}).")
    return render_template("registrar_objeto.html", valores=valores, errores=errores, categorias=CATEGORIAS)


@app.route("/admin/opciones", methods=["GET", "POST"])
@requiere_admin
def opciones():
    """Cambiar nombre, usuario y contraseña del administrador (pide la contraseña actual)."""
    aviso, error = "", False
    if request.method == "POST":
        f = request.form
        resultado = acceso.cambiar_credenciales(f.get("actual", ""), f.get("nombre", ""), f.get("usuario", ""),
                                                f.get("nueva", ""), f.get("confirmar", ""))
        aviso, error = (resultado, True) if resultado else ("Credenciales actualizadas.", False)
    credenciales = almacen.cargar_credenciales()
    return render_template("opciones.html", aviso=aviso, error=error, nombre=credenciales.get("nombre", ""),
                           usuario_admin=credenciales["usuario"])


@app.route("/admin/usuarios", methods=["GET", "POST"])
@requiere_admin
def admin_usuarios():
    """Lista de cuentas: cuándo se registraron, editar sus datos o contraseña, o borrarlas."""
    datos = almacen.cargar()
    aviso, error = "", False
    if request.method == "POST":
        f = request.form
        usuario_id = int(f["usuario_id"])
        if f["accion"] == "borrar":
            usuarios.borrar(datos, usuario_id)
            resultado, aviso = None, "Cuenta borrada."
        else:
            resultado = usuarios.editar(datos, usuario_id, f.get("nombre", ""), f.get("apellido", ""),
                                        f.get("correo", ""), f.get("nueva", ""), f.get("confirmar", ""))
            aviso = resultado or "Cuenta actualizada."
        error = bool(resultado)
        if not error:
            almacen.guardar(datos)
    return render_template("usuarios.html", lista=datos["usuarios"], aviso=aviso, error=error,
                           descripcion=usuarios.descripcion)


if __name__ == "__main__":
    # host="0.0.0.0": acepta conexiones de otros equipos de la misma red (no solo de este)
    app.run(host="0.0.0.0", port=5000, debug=False)
