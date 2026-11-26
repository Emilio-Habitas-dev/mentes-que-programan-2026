"""Ventana principal: barra superior (logo, modo y cambio de rol) y área donde se muestran las vistas."""
import tkinter as tk

from app import datos, estilos
from app.pantallas.admin_login import PantallaLogin
from app.pantallas.admin_panel import PantallaPanelAdmin
from app.pantallas.admin_reportes import PantallaReportes
from app.pantallas.admin_solicitudes import PantallaSolicitudes
from app.pantallas.confirmacion import PantallaConfirmacion
from app.pantallas.detalle import PantallaDetalle
from app.pantallas.inicio import PantallaInicio
from app.pantallas.listado import PantallaListado
from app.pantallas.reclamo import PantallaReclamo
from app.pantallas.reportar import PantallaReportar

# Nombre de cada vista -> clase que la dibuja
PANTALLAS = {
    "inicio": PantallaInicio,
    "listado": PantallaListado,
    "detalle": PantallaDetalle,
    "reclamo": PantallaReclamo,
    "confirmacion": PantallaConfirmacion,
    "login": PantallaLogin,
    "panel_admin": PantallaPanelAdmin,
    "solicitudes": PantallaSolicitudes,
    "reportes": PantallaReportes,
    "reportar": PantallaReportar,
}

# Vistas que se muestran sin la barra superior (tienen su propio diseño de portada)
SIN_BARRA = {"inicio", "login"}


class Ventana:
    def __init__(self, root):
        self.root = root
        root.title("FIND IT · Objetos perdidos y encontrados")
        root.geometry("1180x740")
        root.minsize(920, 620)
        estilos.configurar(root)

        self.datos = datos.cargar()
        self.modo = None  # "estudiante" o "admin" según el rol elegido en Inicio

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
        self.etiqueta_modo = tk.Label(barra, text="", font=estilos.fuente(11), bg=estilos.AZUL_SUAVE,
                                      fg=estilos.TEXTO, padx=14, pady=6)
        self.etiqueta_modo.pack(side="right", padx=10)
        return barra

    def mostrar(self, nombre, **parametros):
        """Cambia la vista. 'parametros' lleva datos extra, por ejemplo objeto_id."""
        for widget in self.contenido.winfo_children():
            widget.destroy()

        # Mostrar u ocultar la barra superior según la vista
        if nombre in SIN_BARRA:
            self.barra.pack_forget()
        else:
            self.barra.pack(fill="x", before=self.contenido)
            es_admin = self.modo == "admin"
            self.etiqueta_modo.configure(text="Modo: Administrador" if es_admin else "Modo: Estudiante / Profesor")
            self.boton_rol.configure(text="Cerrar sesión" if es_admin else "Cambiar rol")

        PANTALLAS[nombre](self.contenido, self, **parametros).pack(fill="both", expand=True)

    def cambiar_rol(self):
        """Vuelve a Inicio para elegir otro rol (si era administrador, cierra la sesión)."""
        self.modo = None
        self.mostrar("inicio")

    def guardar(self):
        datos.guardar(self.datos)

    def restablecer_datos(self):
        """Vuelve a los 10 objetos de prueba (útil antes de la demostración)."""
        datos.restablecer()
        self.datos = datos.cargar()
