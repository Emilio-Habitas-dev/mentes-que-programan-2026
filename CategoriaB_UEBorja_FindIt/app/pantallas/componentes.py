"""Piezas de formulario reutilizables: un campo con etiqueta, control y mensaje de error."""
import tkinter as tk
from tkinter import ttk

from app import estilos
from app.logica.validaciones import MIN_TEXTO


class Campo:
    """Campo de formulario. tipo: "entrada" (una línea), "lista" (desplegable) o "texto" (varias líneas).
    Con contador=True muestra en vivo cuántos caracteres lleva frente al mínimo."""

    def __init__(self, padre, etiqueta, tipo="entrada", opciones=(), ancho=24, contador=False):
        self.tipo = tipo
        self.marco = tk.Frame(padre, bg=estilos.BLANCO)

        cabecera = tk.Frame(self.marco, bg=estilos.BLANCO)
        cabecera.pack(fill="x", pady=(0, 4))
        estilos.texto(cabecera, etiqueta, 11, "bold").pack(side="left")
        estilos.texto(cabecera, " *", 11, "bold", estilos.ERROR).pack(side="left")
        self.contador = estilos.texto(cabecera, "", 10, "bold") if contador else None
        if self.contador:
            self.contador.pack(side="right")

        if tipo == "texto":
            self.control = tk.Text(self.marco, height=3, width=ancho, wrap="word", font=estilos.fuente(11),
                                   relief="flat", highlightthickness=1, highlightbackground=estilos.BORDE,
                                   highlightcolor=estilos.AZUL, padx=8, pady=6)
            self.control.bind("<KeyRelease>", lambda _: self.actualizar_contador())
        else:
            self.variable = tk.StringVar()
            if tipo == "lista":
                self.control = ttk.Combobox(self.marco, textvariable=self.variable, values=list(opciones),
                                            state="readonly", width=ancho)
            else:
                self.control = ttk.Entry(self.marco, textvariable=self.variable, width=ancho)
        self.control.pack(fill="x")

        # El mensaje de error solo ocupa espacio cuando hay un error (ver marcar)
        self.error = estilos.texto(self.marco, "", 10, color=estilos.ERROR)
        self.actualizar_contador()

    def valor(self):
        if self.tipo == "texto":
            return self.control.get("1.0", "end").strip()
        return self.variable.get()

    def actualizar_contador(self):
        """Rojo si aún no llega al mínimo de caracteres, verde si ya cumple."""
        if self.contador:
            largo = len(self.valor())
            color = estilos.VERDE if largo >= MIN_TEXTO else estilos.ERROR
            self.contador.configure(text=f"{largo} / {MIN_TEXTO} caracteres mín.", fg=color)

    def marcar(self, mensaje):
        """Muestra el error (o lo borra si mensaje es vacío) y pinta el campo en rojo."""
        self.error.configure(text=mensaje or "")
        hay_error = bool(mensaje)
        if hay_error:
            self.error.pack(fill="x")
        else:
            self.error.pack_forget()
        if self.tipo == "texto":
            self.control.configure(bg=estilos.ERROR_FONDO if hay_error else estilos.BLANCO,
                                   highlightbackground=estilos.ERROR if hay_error else estilos.BORDE)
        else:
            base = "TCombobox" if self.tipo == "lista" else "TEntry"
            self.control.configure(style=("Invalido." + base) if hay_error else base)


def mostrar_errores(campos, errores):
    """Recorre los campos {clave: Campo} y marca los que tienen error."""
    for clave, campo in campos.items():
        campo.marcar(errores.get(clave))
