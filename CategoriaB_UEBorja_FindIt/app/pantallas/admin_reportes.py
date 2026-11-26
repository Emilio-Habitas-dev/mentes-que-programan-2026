"""Vista Reportes de objetos perdidos (administrador): lo que estudiantes y profesores dicen haber perdido."""
from app.logica import reportes
from app.pantallas.tabla_admin import PantallaTablaAdmin


class PantallaReportes(PantallaTablaAdmin):
    TITULO = "Reportes de objetos perdidos"
    SUBTITULO = "Objetos que la comunidad reportó como perdidos. Márcalos como atendidos al revisarlos."
    VACIO = "No hay reportes pendientes."
    COLUMNAS = {
        "objeto": ("Objeto", 170), "categoria": ("Categoría", 100), "lugar": ("Dónde se perdió", 150),
        "descripcion": ("Descripción", 250), "persona": ("Reportado por", 170), "curso": ("Curso", 90),
        "fecha": ("Fecha", 100),
    }

    def __init__(self, padre, app):
        super().__init__(padre, app, [("Marcar como atendido", self.atender, True)])

    def filas(self):
        return [(r["id"], (r["objeto"], r["categoria"], r["lugar"], r["descripcion"],
                           f"{r['nombre']} {r['apellido']}", r["curso"], r["fecha"]))
                for r in reportes.pendientes(self.app.datos)]

    def atender(self):
        reporte_id = self.seleccionado()
        if reporte_id is None:
            return
        reportes.marcar_atendido(self.app.datos, reporte_id)
        self.app.guardar()
        self.actualizar()
        self.avisar("Reporte marcado como atendido.")
