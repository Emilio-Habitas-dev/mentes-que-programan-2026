"""Vista Buzón de mensajes: avisos del administrador (reporte publicado, dueño encontrado, hora de entrega)."""
import tkinter as tk

from app import estilos
from app.logica import mensajes


class PantallaBuzon(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=16)
        self.app = app
        estilos.boton_enlace(self, "←  Volver al listado", lambda: app.mostrar("listado")).pack(anchor="w")
        estilos.texto(self, "✉  Mis mensajes", 26, "bold", fondo=estilos.FONDO).pack(anchor="w", pady=(0, 12))

        cuerpo = tk.Frame(self, bg=estilos.FONDO)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        izquierda = estilos.tarjeta(cuerpo, relleno=8)
        izquierda.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        self.lista = tk.Listbox(izquierda, width=40, borderwidth=0, highlightthickness=0, activestyle="none",
                                font=estilos.fuente(11), selectbackground=estilos.AZUL)
        self.lista.pack(fill="both", expand=True)
        self.lista.bind("<<ListboxSelect>>", lambda _: self.abrir())

        self.lectura = estilos.tarjeta(cuerpo, relleno=24)
        self.lectura.grid(row=0, column=1, sticky="nsew")
        self.titulo = estilos.texto(self.lectura, "", 18, "bold", wraplength=520)
        self.titulo.pack(anchor="w")
        self.fecha = estilos.texto(self.lectura, "", 10, color=estilos.TEXTO_SUAVE)
        self.fecha.pack(anchor="w", pady=(2, 12))
        self.texto = estilos.texto(self.lectura, "", 12, wraplength=520)
        self.texto.pack(anchor="w")
        self.actualizar()

    def actualizar(self):
        """Lista de mensajes; los no leídos llevan ● al inicio."""
        self.mensajes = mensajes.de_usuario(self.app.datos, self.app.usuario["id"])
        self.lista.delete(0, "end")
        for mensaje in self.mensajes:
            marca = "●" if not mensaje["leido"] else "  "
            self.lista.insert("end", f" {marca}  {mensaje['titulo']}")
        if not self.mensajes:
            self.titulo.configure(text="No tienes mensajes todavía.")
            self.texto.configure(text="Aquí te avisaremos cuando publiquemos tu reporte o encontremos al dueño "
                                      "del objeto, con la hora de entrega en el edificio administrativo.")

    def abrir(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            return
        indice = seleccion[0]
        mensaje = self.mensajes[indice]
        self.titulo.configure(text=mensaje["titulo"])
        self.fecha.configure(text=mensaje["fecha"])
        self.texto.configure(text=mensaje["texto"])
        if not mensaje["leido"]:
            mensajes.marcar_leido(self.app.datos, mensaje["id"])
            self.app.guardar()
            self.actualizar()
            self.lista.selection_set(indice)
            self.app.actualizar_barra()  # baja el contador del ícono ✉
