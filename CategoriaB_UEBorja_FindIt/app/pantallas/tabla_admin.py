"""Base común de las vistas del administrador que muestran una tabla con acciones (solicitudes y reportes)."""
import tkinter as tk
from tkinter import ttk

from app import estilos


class PantallaTablaAdmin(tk.Frame):
    """Título, tabla en tarjeta, mensaje de resultado y botones de acción abajo.
    Las clases hijas definen COLUMNAS, filas() y las acciones."""

    COLUMNAS = {}
    TITULO = ""
    SUBTITULO = ""
    VACIO = ""

    def __init__(self, padre, app, acciones):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=16)
        self.app = app
        estilos.boton_enlace(self, "←  Volver al panel", lambda: app.mostrar("panel_admin")).pack(anchor="w")
        estilos.texto(self, self.TITULO, 26, "bold", fondo=estilos.FONDO).pack(anchor="w", pady=(4, 0))
        estilos.texto(self, self.SUBTITULO, 12, color=estilos.TEXTO_SUAVE, fondo=estilos.FONDO).pack(
            anchor="w", pady=(0, 14))

        abajo = tk.Frame(self, bg=estilos.FONDO)
        abajo.pack(side="bottom", fill="x", pady=(12, 0))
        self.mensaje = estilos.texto(abajo, "", 11, fondo=estilos.FONDO)
        self.mensaje.pack(side="left")
        for indice, (texto, comando, principal) in enumerate(reversed(acciones)):
            crear = estilos.boton_primario if principal else estilos.boton_secundario
            crear(abajo, texto, comando).pack(side="right", padx=(10 if indice else 0, 0))

        marco = estilos.tarjeta(self, relleno=0)
        marco.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(marco, columns=list(self.COLUMNAS), show="headings", selectmode="browse")
        for clave, (titulo, ancho) in self.COLUMNAS.items():
            self.tabla.heading(clave, text=titulo, anchor="w")
            self.tabla.column(clave, width=ancho, minwidth=50, anchor="w")
        self.tabla.pack(fill="both", expand=True)
        self.vacio = estilos.texto(marco, self.VACIO, 13, color=estilos.TEXTO_SUAVE, anchor="center")
        self.actualizar()

    def filas(self):
        """Lista de (id, valores) a mostrar. La define cada vista."""
        return []

    def actualizar(self):
        self.tabla.delete(*self.tabla.get_children())
        filas = self.filas()
        for identificador, valores in filas:
            self.tabla.insert("", "end", iid=str(identificador), values=valores)
        if filas:
            self.vacio.place_forget()
        else:
            self.vacio.place(relx=0.5, rely=0.5, anchor="center")

    def seleccionado(self):
        """Id de la fila seleccionada, o None (y avisa)."""
        seleccion = self.tabla.selection()
        if not seleccion:
            self.avisar("Selecciona una fila de la tabla.", error=True)
            return None
        return int(seleccion[0])

    def avisar(self, texto, error=False):
        self.mensaje.configure(text=texto, fg=estilos.ERROR if error else estilos.VERDE)
