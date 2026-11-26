"""Vista Reportar objeto perdido (estudiante o profesor): avisa a Inspección qué perdió."""
import tkinter as tk

from app import estilos
from app.logica import reportes
from app.logica.validaciones import CATEGORIAS, GRADOS, PARALELOS
from app.pantallas.componentes import Campo, mostrar_errores


class PantallaReportar(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=16)
        self.app = app
        estilos.boton_enlace(self, "←  Volver al listado", lambda: app.mostrar("listado")).pack(anchor="w")

        tarjeta = estilos.tarjeta(self, relleno=26)
        tarjeta.pack(pady=(6, 0))
        estilos.texto(tarjeta, "Reportar objeto perdido", 22, "bold").grid(row=0, column=0, columnspan=2, sticky="w")
        estilos.texto(tarjeta, "Cuéntale a Inspección qué perdiste. Si lo encuentran, aparecerá en el listado.",
                      11, color=estilos.TEXTO_SUAVE).grid(row=1, column=0, columnspan=2, sticky="w", pady=(2, 10))

        self.campos = {
            "nombre": Campo(tarjeta, "Nombre"),
            "apellido": Campo(tarjeta, "Apellido"),
            "grado": Campo(tarjeta, "Grado", "lista", GRADOS),
            "paralelo": Campo(tarjeta, "Paralelo", "lista", PARALELOS),
            "objeto": Campo(tarjeta, "Objeto perdido"),
            "categoria": Campo(tarjeta, "Categoría", "lista", CATEGORIAS),
            "lugar": Campo(tarjeta, "Dónde lo perdiste"),
            "descripcion": Campo(tarjeta, "Descripción del objeto", "texto", ancho=52, contador=True),
        }
        orden = ["nombre", "apellido", "grado", "paralelo", "objeto", "categoria"]
        for indice, clave in enumerate(orden):
            fila, columna = 2 + indice // 2, indice % 2
            self.campos[clave].marco.grid(row=fila, column=columna, sticky="ew",
                                          padx=(0, 10) if columna == 0 else (10, 0), pady=3)
        self.campos["lugar"].marco.grid(row=5, column=0, columnspan=2, sticky="ew", pady=3)
        self.campos["descripcion"].marco.grid(row=6, column=0, columnspan=2, sticky="ew", pady=3)

        botones = tk.Frame(tarjeta, bg=estilos.BLANCO)
        botones.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        estilos.boton_primario(botones, "Enviar reporte", self.enviar).pack(side="right")
        estilos.boton_secundario(botones, "Cancelar", lambda: app.mostrar("listado")).pack(side="right", padx=10)
        self.campos["nombre"].control.focus()

    def enviar(self):
        valores = {clave: campo.valor() for clave, campo in self.campos.items()}
        errores, reporte = reportes.registrar_reporte(self.app.datos, **valores)
        if errores:
            mostrar_errores(self.campos, errores)
            return
        self.app.guardar()
        self.app.mostrar("confirmacion", exito=True, titulo="¡Reporte enviado!",
                         detalle=f"Inspección buscará tu «{reporte['objeto']}».\n"
                                 "Revisa el listado de objetos encontrados en los próximos días.")
