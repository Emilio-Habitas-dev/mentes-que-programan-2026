"""Vista Reportar objeto encontrado (estudiante o profesor): avisa a Inspección que encontró un objeto."""
import tkinter as tk

from app import estilos
from app.logica import reportes
from app.logica.validaciones import CATEGORIAS, GRADOS, PARALELOS
from app.pantallas.componentes import Campo, mostrar_errores


class PantallaReportar(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=12)
        self.app = app
        estilos.boton_enlace(self, "←  Volver al listado", lambda: app.mostrar("listado")).pack(anchor="w")

        tarjeta = estilos.tarjeta(self, relleno=22)
        tarjeta.pack(pady=(4, 0))
        estilos.texto(tarjeta, "Reportar objeto encontrado", 22, "bold").grid(row=0, column=0, columnspan=2, sticky="w")
        estilos.texto(tarjeta, "¿Encontraste algo? Llévalo a Inspección y repórtalo aquí: cuando lo reciban, "
                               "aparecerá en el listado.", 11, color=estilos.TEXTO_SUAVE, wraplength=520).grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(2, 8))

        self.campos = {
            "nombre": Campo(tarjeta, "Nombre"),
            "apellido": Campo(tarjeta, "Apellido"),
            "correo": Campo(tarjeta, "Correo institucional"),
            "grado": Campo(tarjeta, "Grado", "lista", GRADOS),
            "paralelo": Campo(tarjeta, "Paralelo", "lista", PARALELOS),
            "objeto": Campo(tarjeta, "Objeto encontrado"),
            "categoria": Campo(tarjeta, "Categoría", "lista", CATEGORIAS),
            "lugar": Campo(tarjeta, "Dónde lo encontraste"),
            "descripcion": Campo(tarjeta, "Descripción del objeto", "texto", ancho=52, contador=True),
        }
        # (fila, columna); columna None = ocupa las dos columnas
        posiciones = {"nombre": (2, 0), "apellido": (2, 1), "correo": (3, None), "grado": (4, 0),
                      "paralelo": (4, 1), "objeto": (5, 0), "categoria": (5, 1), "lugar": (6, None),
                      "descripcion": (7, None)}
        for clave, (fila, columna) in posiciones.items():
            if columna is None:
                self.campos[clave].marco.grid(row=fila, column=0, columnspan=2, sticky="new", pady=2)
            else:
                self.campos[clave].marco.grid(row=fila, column=columna, sticky="new", pady=2,
                                              padx=(0, 10) if columna == 0 else (10, 0))
        self.campos["descripcion"].control.configure(height=2)

        botones = tk.Frame(tarjeta, bg=estilos.BLANCO)
        botones.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(8, 0))
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
        self.app.mostrar("confirmacion", exito=True, titulo="¡Gracias por reportarlo!",
                         detalle=f"Lleva «{reporte['objeto']}» a Inspección.\n"
                                 "Cuando lo reciban, aparecerá en el listado para que su dueño lo reclame.")
