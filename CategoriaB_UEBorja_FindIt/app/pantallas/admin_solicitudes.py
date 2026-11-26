"""Vista Solicitudes de reclamo (administrador): reclamos registrados en la app, para entregar o rechazar."""
from tkinter import messagebox, simpledialog

from app.logica import objetos, reclamos
from app.pantallas.tabla_admin import PantallaTablaAdmin


class PantallaSolicitudes(PantallaTablaAdmin):
    TITULO = "Solicitudes de reclamo"
    SUBTITULO = "Compara la seña: coordina la hora de entrega (avisa al dueño y a quien lo encontró), luego márcalo entregado."
    VACIO = "No hay solicitudes pendientes. Aparecerán aquí cuando alguien reclame un objeto."
    COLUMNAS = {
        "objeto": ("Objeto", 160), "nombre": ("Reclamado por", 140), "correo": ("Correo", 200),
        "curso": ("Curso", 85), "sena": ("Seña particular", 200), "fecha": ("Fecha", 90),
        "estado": ("Estado / hora", 130),
    }

    def __init__(self, padre, app):
        super().__init__(padre, app, [("Rechazar", self.rechazar, False),
                                      ("Coordinar entrega", self.coordinar, False),
                                      ("Marcar como entregado", self.entregar, True)])

    def filas(self):
        """Solo reclamos hechos en la app y aún pendientes (no se inventan solicitudes iniciales)."""
        filas = []
        for reclamo in reclamos.pendientes(self.app.datos):
            objeto = objetos.buscar_por_id(self.app.datos, reclamo["objeto_id"])
            persona = f"{reclamo['nombre']} {reclamo.get('apellido', '')}".strip()
            estado = (f"Entrega {reclamo['hora_entrega']}" if reclamo.get("estado") == reclamos.COORDINADO
                      else "Pendiente")
            filas.append((reclamo["id"], (objeto["nombre"], persona, reclamo.get("correo", "—"), reclamo["curso"],
                                          reclamo["sena"], reclamo["fecha"], estado)))
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

    def coordinar(self):
        """Pide la hora y envía los mensajes al dueño y a quien encontró el objeto."""
        reclamo_id = self.seleccionado()
        if reclamo_id is None:
            return
        hora = simpledialog.askstring("Coordinar entrega", "Hora de entrega en el edificio administrativo (HH:MM):",
                                      parent=self)
        if hora is None:
            return
        error = reclamos.coordinar_entrega(self.app.datos, reclamo_id, hora)
        if error:
            self.avisar(error, error=True)
            return
        self.app.guardar()
        self.actualizar()
        self.avisar(f"Entrega coordinada a las {hora.strip()}. Se enviaron los mensajes.")

    def entregar(self):
        self._resolver(reclamos.entregar, "¿El dueño ya retiró el objeto? Pasará a Entregado.",
                       "Objeto marcado como Entregado.")

    def rechazar(self):
        self._resolver(reclamos.rechazar, "¿Rechazar el reclamo? El objeto volverá a estar Disponible.",
                       "Reclamo rechazado. El objeto volvió a Disponible.")
