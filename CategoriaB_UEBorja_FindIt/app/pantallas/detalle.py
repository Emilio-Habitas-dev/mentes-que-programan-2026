"""Vista Detalle: ícono ilustrativo, información completa del objeto y botón «Reclamar objeto»."""
import tkinter as tk
from tkinter import messagebox

from app import datos, estilos
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
        self._imagen(izquierda, objeto).pack(expand=True, pady=10)
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

        # El administrador no reclama: en su lugar puede borrar el objeto del listado
        if app.modo == "admin":
            boton = estilos.boton_primario(derecha, "Borrar objeto del listado", lambda: self.borrar(app, objeto))
            boton.configure(bg=estilos.ERROR, activebackground="#7F1D1D")
            boton.pack(fill="x", pady=(18, 0))
            self.mensaje = estilos.texto(derecha, "", 10, color=estilos.ERROR, wraplength=420)
            self.mensaje.pack(anchor="w", pady=(6, 0))
            return

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

    def _imagen(self, padre, objeto):
        """Foto del objeto si la tiene (reducida a ~260 px); si no, el ícono de su categoría."""
        ruta = datos.ruta_foto(objeto.get("foto"))
        if ruta:
            try:
                foto = tk.PhotoImage(file=str(ruta))
                factor = max(1, -(-max(foto.width(), foto.height()) // 260))  # división hacia arriba
                self.foto = foto.subsample(factor)  # se guarda en self para que no se borre de memoria
                return tk.Label(padre, image=self.foto, bg=estilos.BLANCO)
            except tk.TclError:
                pass  # Archivo dañado: se usa el ícono
        return estilos.icono_categoria(padre, objeto["categoria"], 260)

    def borrar(self, app, objeto):
        if not messagebox.askyesno("Borrar objeto", f"¿Borrar «{objeto['nombre']}» del listado?"):
            return
        error = objetos.borrar_objeto(app.datos, objeto["id"])
        if error:
            self.mensaje.configure(text=error)
            return
        app.guardar()
        app.mostrar("listado")
