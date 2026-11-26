"""Vista Solicitudes de reclamo (administrador): reclamos registrados en la app, para entregar o rechazar."""
from tkinter import messagebox

from app.logica import objetos, reclamos
from app.pantallas.tabla_admin import PantallaTablaAdmin


class PantallaSolicitudes(PantallaTablaAdmin):
    TITULO = "Solicitudes de reclamo"
    SUBTITULO = "Compara la seña particular con el objeto: entrégalo a su dueño o rechaza el reclamo."
    VACIO = "No hay solicitudes pendientes. Aparecerán aquí cuando alguien reclame un objeto."
    COLUMNAS = {
        "objeto": ("Objeto", 170), "nombre": ("Reclamado por", 150), "correo": ("Correo", 220),
        "curso": ("Curso", 90), "sena": ("Seña particular", 230), "fecha": ("Fecha", 95),
    }

    def __init__(self, padre, app):
        super().__init__(padre, app, [("Rechazar reclamo", self.rechazar, False),
                                      ("Marcar como entregado", self.entregar, True)])

    def filas(self):
        """Solo reclamos hechos en la app y aún pendientes (no se inventan solicitudes iniciales)."""
        filas = []
        for reclamo in reclamos.pendientes(self.app.datos):
            objeto = objetos.buscar_por_id(self.app.datos, reclamo["objeto_id"])
            persona = f"{reclamo['nombre']} {reclamo.get('apellido', '')}".strip()
            filas.append((reclamo["id"], (objeto["nombre"], persona, reclamo.get("correo", "—"), reclamo["curso"],
                                          reclamo["sena"], reclamo["fecha"])))
        return filas

    def _resolver(self, accion, pregunta, exito):
        reclamo_id = self.seleccionado()
        if reclamo_id is None or not messagebox.askyesno("Confirmar", pregunta):
            return
        error = accion(self.app.datos, reclamo_id)
        if error:
            self.avisar(error, error=True)
            return
        self.app.guardar()
        self.actualizar()
        self.avisar(exito)

    def entregar(self):
        self._resolver(reclamos.entregar, "¿El dueño ya retiró el objeto? Pasará a Entregado.",
                       "Objeto marcado como Entregado.")

    def rechazar(self):
        self._resolver(reclamos.rechazar, "¿Rechazar el reclamo? El objeto volverá a estar Disponible.",
                       "Reclamo rechazado. El objeto volvió a Disponible.")
