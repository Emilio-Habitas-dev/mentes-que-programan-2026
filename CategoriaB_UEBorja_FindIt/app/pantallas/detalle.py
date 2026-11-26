"""Vista Detalle: ícono ilustrativo, información completa del objeto y botón «Reclamar objeto»."""
import tkinter as tk

from app import estilos
from app.logica import objetos, reclamos


class PantallaDetalle(tk.Frame):
    def __init__(self, padre, app, objeto_id):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=20)
        objeto = objetos.buscar_por_id(app.datos, objeto_id)

        estilos.boton_enlace(self, "←  Volver al listado", lambda: app.mostrar("listado")).pack(anchor="w")

        cuerpo = tk.Frame(self, bg=estilos.FONDO)
        cuerpo.pack(fill="both", expand=True, pady=(12, 0))
        cuerpo.columnconfigure(0, weight=1, uniform="columnas")
        cuerpo.columnconfigure(1, weight=1, uniform="columnas")

        # Izquierda: ícono de la categoría y número de ID
        izquierda = estilos.tarjeta(cuerpo)
        izquierda.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        tk.Label(izquierda, text=f" ID #{objeto['id']:02d} ", font=estilos.fuente(11, "bold"),
                 fg=estilos.BLANCO, bg=estilos.MARINO, pady=4).pack(anchor="e")
        estilos.icono_categoria(izquierda, objeto["categoria"], 260).pack(expand=True, pady=10)
        estilos.texto(izquierda, objeto["categoria"], 13, "bold", estilos.TEXTO_SUAVE, anchor="center").pack()

        # Derecha: estado, nombre, datos y botón Reclamar
        derecha = estilos.tarjeta(cuerpo, relleno=28)
        derecha.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        estilos.chip_estado(derecha, objeto["estado"]).pack(anchor="w")
        estilos.texto(derecha, objeto["nombre"], 24, "bold", wraplength=440).pack(anchor="w", pady=(10, 14))

        campos = [("Categoría", objeto["categoria"]), ("Lugar del hallazgo", objeto["lugar"]),
                  ("Fecha del hallazgo", objeto["fecha_hallazgo"]), ("Descripción", objeto["descripcion"])]
        if objeto["fecha_entrega"]:
            campos.append(("Fecha de entrega", objeto["fecha_entrega"]))
        for campo, valor in campos:
            fila = tk.Frame(derecha, bg=estilos.BLANCO)
            fila.pack(fill="x", pady=4)
            estilos.texto(fila, f"{campo}:", 12, "bold").pack(side="left")
            estilos.texto(fila, valor, 12, wraplength=320).pack(side="left", padx=6)

        # Mensaje informativo y botón; la regla de si se puede reclamar está en logica/reclamos.py
        se_puede = reclamos.puede_reclamar(objeto)
        aviso = ("¿Reconoces este objeto como tuyo? Registra un reclamo con una seña particular "
                 "para validarlo en Inspección." if se_puede else
                 f"Este objeto ya está {objeto['estado']}, por eso no se puede reclamar.")
        caja = tk.Frame(derecha, bg=estilos.AZUL_SUAVE, padx=16, pady=12)
        caja.pack(fill="x", pady=(18, 16))
        estilos.texto(caja, "ⓘ  " + aviso, 11, fondo=estilos.AZUL_SUAVE, wraplength=420).pack(anchor="w")

        boton = estilos.boton_primario(derecha, "Reclamar objeto",
                                       lambda: app.mostrar("reclamo", objeto_id=objeto_id))
        boton.pack(fill="x")
        if not se_puede:
            estilos.desactivar(boton)
