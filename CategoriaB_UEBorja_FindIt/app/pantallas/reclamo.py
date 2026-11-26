"""Vista Formulario de reclamo: nombre, apellido, grado, paralelo y seña particular, con validación."""
import tkinter as tk

from app import estilos
from app.logica import objetos, reclamos
from app.logica.validaciones import GRADOS, PARALELOS
from app.pantallas.componentes import Campo, mostrar_errores


class PantallaReclamo(tk.Frame):
    def __init__(self, padre, app, objeto_id):
        super().__init__(padre, bg=estilos.FONDO, padx=32, pady=16)
        self.app = app
        self.objeto_id = objeto_id
        self.objeto = objetos.buscar_por_id(app.datos, objeto_id)

        estilos.boton_enlace(self, "←  Volver al detalle",
                             lambda: app.mostrar("detalle", objeto_id=objeto_id)).pack(anchor="w")

        tarjeta = estilos.tarjeta(self, relleno=26)
        tarjeta.pack(pady=(6, 0))
        estilos.texto(tarjeta, "Formulario de reclamo", 22, "bold").grid(row=0, column=0, columnspan=2, sticky="w")
        resumen = tk.Frame(tarjeta, bg=estilos.AZUL_SUAVE, padx=14, pady=10)
        resumen.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(8, 12))
        estilos.texto(resumen, f"{self.objeto['nombre']}  ·  {self.objeto['lugar']}  ·  "
                               f"{self.objeto['fecha_hallazgo']}", 11, fondo=estilos.AZUL_SUAVE).pack(anchor="w")

        # Campos en dos columnas: nombre | apellido, grado | paralelo; correo y seña ocupan todo el ancho
        self.campos = {
            "nombre": Campo(tarjeta, "Nombre"),
            "apellido": Campo(tarjeta, "Apellido"),
            "correo": Campo(tarjeta, "Correo (de preferencia institucional)"),
            "grado": Campo(tarjeta, "Grado", "lista", GRADOS),
            "paralelo": Campo(tarjeta, "Paralelo", "lista", PARALELOS),
            "sena": Campo(tarjeta, "Seña particular del objeto", "texto", ancho=52, contador=True),
        }
        posiciones = {"nombre": (2, 0), "apellido": (2, 1), "grado": (4, 0), "paralelo": (4, 1)}
        for clave, (fila, columna) in posiciones.items():
            self.campos[clave].marco.grid(row=fila, column=columna, sticky="new",
                                          padx=(0, 10) if columna == 0 else (10, 0), pady=4)
        self.campos["correo"].marco.grid(row=3, column=0, columnspan=2, sticky="ew", pady=4)
        self.campos["sena"].marco.grid(row=5, column=0, columnspan=2, sticky="ew", pady=4)
        estilos.texto(tarjeta, "Ej. de correo: nombre.apellido@colegio.edu.ec  ·  Si eres docente no necesitas paralelo.",
                      10, color=estilos.TEXTO_SUAVE).grid(
            row=6, column=0, columnspan=2, sticky="w")

        botones = tk.Frame(tarjeta, bg=estilos.BLANCO)
        botones.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        estilos.boton_primario(botones, "Enviar reclamo", self.enviar).pack(side="right")
        estilos.boton_secundario(botones, "Cancelar",
                                 lambda: app.mostrar("detalle", objeto_id=objeto_id)).pack(side="right", padx=10)
        self.campos["nombre"].control.focus()

    def enviar(self):
        """Valida y registra. Si hay errores los muestra bajo cada campo y no guarda nada."""
        valores = {clave: campo.valor() for clave, campo in self.campos.items()}
        errores, _ = reclamos.registrar_reclamo(self.app.datos, self.objeto_id, **valores)
        if "general" in errores:  # El objeto ya no está Disponible: se informa en Confirmación
            self.app.mostrar("confirmacion", exito=False, titulo="No se pudo registrar el reclamo",
                             detalle=errores["general"], objeto_id=self.objeto_id)
            return
        if errores:
            mostrar_errores(self.campos, errores)
            return
        self.app.guardar()
        self.app.mostrar("confirmacion", exito=True, titulo="¡Reclamo registrado!",
                         detalle=f"El objeto «{self.objeto['nombre']}» ahora está Reclamado.\n"
                                 "Acércate a Inspección con tu seña particular para retirarlo.")
