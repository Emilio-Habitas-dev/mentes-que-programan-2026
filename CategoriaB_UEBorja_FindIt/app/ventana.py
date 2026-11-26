"""Ventana principal: barra superior (logo, modo y cambio de rol) y área donde se muestran las vistas."""
import tkinter as tk

from app import datos, estilos, sonido
from app.logica import mensajes, usuarios
from app.pantallas.acceso import PantallaAcceso
from app.pantallas.admin_login import PantallaLogin
from app.pantallas.admin_panel import PantallaPanelAdmin
from app.pantallas.admin_reportes import PantallaReportes
from app.pantallas.admin_solicitudes import PantallaSolicitudes
from app.pantallas.buzon import PantallaBuzon
from app.pantallas.confirmacion import PantallaConfirmacion
from app.pantallas.detalle import PantallaDetalle
from app.pantallas.inicio import PantallaInicio
from app.pantallas.listado import PantallaListado
from app.pantallas.reclamo import PantallaReclamo
from app.pantallas.registrar_objeto import PantallaRegistrarObjeto
from app.pantallas.reportar import PantallaReportar

# Nombre de cada vista -> clase que la dibuja
PANTALLAS = {
    "inicio": PantallaInicio,
    "acceso": PantallaAcceso,
    "buzon": PantallaBuzon,
    "listado": PantallaListado,
    "detalle": PantallaDetalle,
    "reclamo": PantallaReclamo,
    "confirmacion": PantallaConfirmacion,
    "login": PantallaLogin,
    "panel_admin": PantallaPanelAdmin,
    "solicitudes": PantallaSolicitudes,
    "reportes": PantallaReportes,
    "reportar": PantallaReportar,
    "registrar_objeto": PantallaRegistrarObjeto,
}

# Vistas que se muestran sin la barra superior (tienen su propio diseño de portada)
SIN_BARRA = {"inicio", "login", "acceso"}


class Ventana:
    def __init__(self, root):
        self.root = root
        root.title("FIND IT · Objetos perdidos y encontrados")
        root.geometry("1180x780")
        root.minsize(920, 620)
        estilos.configurar(root)
        sonido.activar(root)  # clic al pulsar cualquier botón

        self.datos = datos.cargar()
        self.modo = None  # "estudiante" o "admin" según el rol elegido en Inicio
        self.usuario = None  # Cuenta del estudiante o profesor que inició sesión

        self.barra = self._crear_barra()
        self.contenido = tk.Frame(root, bg=estilos.FONDO)
        self.contenido.pack(fill="both", expand=True)
        self.mostrar("inicio")

    def _crear_barra(self):
        """Barra blanca superior: logo FIND IT a la izquierda; modo y botón de rol a la derecha."""
        barra = tk.Frame(self.root, bg=estilos.BLANCO, padx=28, pady=12,
                         highlightthickness=1, highlightbackground=estilos.BORDE)
        estilos.logo(barra, estilos.BLANCO, 36).pack(side="left")
        estilos.texto(barra, "FIND IT", 20, "bold", estilos.MARINO).pack(side="left", padx=10)

        self.boton_rol = estilos.boton_secundario(barra, "Cambiar rol", self.cambiar_rol)
        self.boton_rol.pack(side="right")
        # Ícono de mensajes con el número de no leídos (solo estudiantes/profesores)
        self.boton_buzon = estilos.boton_secundario(barra, "✉", lambda: self.mostrar("buzon"))
        self.boton_buzon.configure(font=estilos.fuente(13, "bold"))
        self.etiqueta_modo = tk.Label(barra, text="", font=estilos.fuente(11), bg=estilos.AZUL_SUAVE,
                                      fg=estilos.TEXTO, padx=14, pady=6)
        self.etiqueta_modo.pack(side="right", padx=10)
        return barra

    def mostrar(self, nombre, **parametros):
        """Cambia la vista. 'parametros' lleva datos extra, por ejemplo objeto_id."""
        for widget in self.contenido.winfo_children():
            widget.destroy()
        self.recargar()

        # Mostrar u ocultar la barra superior según la vista
        if nombre in SIN_BARRA:
            self.barra.pack_forget()
        else:
            self.barra.pack(fill="x", before=self.contenido)
            self.actualizar_barra()

        PANTALLAS[nombre](self.contenido, self, **parametros).pack(fill="both", expand=True)

    def actualizar_barra(self):
        """Texto del modo/usuario y contador de mensajes no leídos."""
        if self.modo == "admin":
            self.etiqueta_modo.configure(text="Modo: Administrador")
            self.boton_rol.configure(text="Cerrar sesión")
            self.boton_buzon.pack_forget()
            return
        self.boton_rol.configure(text="Cerrar sesión" if self.usuario else "Cambiar rol")
        if self.usuario:
            self.etiqueta_modo.configure(text=f"{self.usuario['nombre']} {self.usuario['apellido']} · "
                                              f"{usuarios.descripcion(self.usuario)}")
            pendientes = mensajes.no_leidos(self.datos, self.usuario["id"])
            self.boton_buzon.configure(text=f"✉  {pendientes}" if pendientes else "✉",
                                       bg=estilos.AMARILLO if pendientes else estilos.BLANCO)
            self.boton_buzon.pack(side="right", padx=(10, 0), before=self.boton_rol)
        else:
            self.etiqueta_modo.configure(text="Modo: Estudiante / Profesor")
            self.boton_buzon.pack_forget()

    def iniciar_sesion_usuario(self, usuario):
        self.modo = "estudiante"
        self.usuario = usuario
        self.mostrar("listado")

    def cambiar_rol(self):
        """Cierra la sesión (usuario o administrador) y vuelve a Inicio."""
        self.modo = None
        self.usuario = None
        self.mostrar("inicio")

    def recargar(self):
        """Vuelve a leer el archivo. Así, si hay otra ventana de FIND IT abierta, se ven sus cambios
        (cuentas nuevas, reclamos, mensajes) y no se borran al guardar."""
        self.datos = datos.cargar()
        if self.usuario:  # la cuenta con la sesión iniciada, con sus datos actualizados
            self.usuario = usuarios.buscar_por_id(self.datos, self.usuario["id"]) or self.usuario

    def guardar(self):
        datos.guardar(self.datos)

    def restablecer_datos(self):
        """Vuelve a los 10 objetos de prueba (útil antes de la demostración). Borra también cuentas y mensajes."""
        datos.restablecer()
        self.datos = datos.cargar()
