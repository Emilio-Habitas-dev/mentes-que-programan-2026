"""Vista Registrar objeto perdido (administrador): agrega directamente un objeto al listado, sin datos de personas."""
import tkinter as tk
from datetime import date

from app import estilos
from app.logica import objetos
from app.logica.validaciones import CATEGORIAS
from app.pantallas.componentes import Campo, mostrar_errores


class PantallaRegistrarObjeto(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=16)
        self.app = app
        estilos.boton_enlace(self, "←  Volver al listado", lambda: app.mostrar("listado")).pack(anchor="w")

        tarjeta = estilos.tarjeta(self, relleno=26)
        tarjeta.pack(pady=(6, 0))
        estilos.texto(tarjeta, "Registrar objeto perdido", 22, "bold").grid(row=0, column=0, columnspan=2, sticky="w")
        estilos.texto(tarjeta, "El objeto se agrega al listado como Disponible.", 11,
                      color=estilos.TEXTO_SUAVE).grid(row=1, column=0, columnspan=2, sticky="w", pady=(2, 10))

        self.campos = {
            "nombre": Campo(tarjeta, "Objeto"),
            "categoria": Campo(tarjeta, "Categoría", "lista", CATEGORIAS),
            "lugar": Campo(tarjeta, "Lugar del hallazgo"),
            "fecha": Campo(tarjeta, "Fecha del hallazgo (AAAA-MM-DD)"),
            "descripcion": Campo(tarjeta, "Descripción", "texto", ancho=52, contador=True),
        }
        self.campos["fecha"].variable.set(date.today().isoformat())  # por defecto, hoy
        posiciones = {"nombre": (2, 0), "categoria": (2, 1), "lugar": (3, 0), "fecha": (3, 1)}
        for clave, (fila, columna) in posiciones.items():
            self.campos[clave].marco.grid(row=fila, column=columna, sticky="new", pady=3,
                                          padx=(0, 10) if columna == 0 else (10, 0))
        self.campos["descripcion"].marco.grid(row=4, column=0, columnspan=2, sticky="ew", pady=3)

        botones = tk.Frame(tarjeta, bg=estilos.BLANCO)
        botones.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        estilos.boton_primario(botones, "Registrar objeto", self.registrar).pack(side="right")
        estilos.boton_secundario(botones, "Cancelar", lambda: app.mostrar("listado")).pack(side="right", padx=10)
        self.campos["nombre"].control.focus()

    def registrar(self):
        valores = {clave: campo.valor() for clave, campo in self.campos.items()}
        errores, objeto = objetos.registrar_objeto(self.app.datos, **valores)
        if errores:
            mostrar_errores(self.campos, errores)
            return
        self.app.guardar()
        self.app.mostrar("confirmacion", exito=True, titulo="¡Objeto registrado!",
                         detalle=f"«{objeto['nombre']}» ya está en el listado como Disponible (ID {objeto['id']:02d}).")
