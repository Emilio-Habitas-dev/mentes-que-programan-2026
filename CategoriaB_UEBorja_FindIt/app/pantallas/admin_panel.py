"""Vista Panel del administrador: tarjetas de acceso a sus funciones (según el boceto 03)."""
import tkinter as tk
from tkinter import messagebox

from app import estilos
from app.logica import reclamos, reportes


class PantallaPanelAdmin(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=24)
        self.app = app
        estilos.texto(self, "¡Bienvenido/a, Administrador/a!", 26, "bold", fondo=estilos.FONDO).pack(anchor="w")
        estilos.texto(self, "Elige qué quieres gestionar.", 12, color=estilos.TEXTO_SUAVE,
                      fondo=estilos.FONDO).pack(anchor="w", pady=(0, 18))

        rejilla = tk.Frame(self, bg=estilos.FONDO)
        rejilla.pack(fill="both", expand=True)
        for columna in (0, 1):
            rejilla.columnconfigure(columna, weight=1, uniform="tarjetas")
        for fila in (0, 1):
            rejilla.rowconfigure(fila, weight=1, uniform="tarjetas")

        tarjetas = [
            ("✉", "Revisar solicitudes de reclamo", "Entrega el objeto a su dueño o rechaza el reclamo.",
             len(reclamos.pendientes(app.datos)), lambda: app.mostrar("solicitudes")),
            ("!", "Revisar reportes de objetos perdidos", "Lo que estudiantes y profesores reportaron como perdido.",
             len(reportes.pendientes(app.datos)), lambda: app.mostrar("reportes")),
            ("✎", "Revisar objetos encontrados", "Consulta la tabla completa de objetos.",
             None, lambda: app.mostrar("listado")),
            ("⚙", "Opciones", "Restablecer los 10 objetos de prueba.", None, self.restablecer),
        ]
        for indice, (icono, titulo, descripcion, contador, accion) in enumerate(tarjetas):
            self._tarjeta(rejilla, indice // 2, indice % 2, icono, titulo, descripcion, contador, accion)

    def _tarjeta(self, rejilla, fila, columna, icono, titulo, descripcion, contador, accion):
        """Tarjeta clicable. Sin acción, se muestra en gris (función aún no disponible)."""
        tarjeta = estilos.tarjeta(rejilla, relleno=24)
        tarjeta.grid(row=fila, column=columna, sticky="nsew", padx=10, pady=10)
        color = estilos.MARINO if accion else estilos.GRIS_DESACTIVADO

        cabecera = tk.Frame(tarjeta, bg=estilos.BLANCO)
        cabecera.pack(fill="x")
        estilos.texto(cabecera, icono, 30, "bold", color).pack(side="left")
        if contador is not None:
            tk.Label(cabecera, text=f" {contador} ", font=estilos.fuente(14, "bold"), fg=estilos.BLANCO,
                     bg=estilos.MARINO, padx=6, pady=2).pack(side="right", anchor="n")
        estilos.texto(tarjeta, titulo, 17, "bold", color, wraplength=360).pack(anchor="w", pady=(10, 4))
        estilos.texto(tarjeta, descripcion, 11, color=estilos.TEXTO_SUAVE, wraplength=360).pack(anchor="w")

        if accion:
            # Toda la tarjeta (y lo que tiene dentro) responde al clic
            for widget in [tarjeta, cabecera] + tarjeta.winfo_children() + cabecera.winfo_children():
                widget.bind("<Button-1>", lambda _: accion())
                widget.configure(cursor="hand2")

    def restablecer(self):
        if messagebox.askyesno("Restablecer datos", "¿Volver a los 10 objetos de prueba?\n"
                                                     "Se borrarán los reclamos y cambios hechos."):
            self.app.restablecer_datos()
            self.app.mostrar("panel_admin")
