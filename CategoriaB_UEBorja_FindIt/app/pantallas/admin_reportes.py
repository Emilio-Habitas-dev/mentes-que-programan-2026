"""Vista Reportes de objetos encontrados (administrador): al recibir el objeto se agrega al listado."""
from tkinter import messagebox

from app.logica import reportes
from app.pantallas.tabla_admin import PantallaTablaAdmin


class PantallaReportes(PantallaTablaAdmin):
    TITULO = "Reportes de objetos encontrados"
    SUBTITULO = "Cuando el estudiante entregue el objeto en Inspección, agrégalo al listado con un clic."
    VACIO = "No hay reportes pendientes."
    COLUMNAS = {
        "objeto": ("Objeto", 150), "categoria": ("Categoría", 95), "lugar": ("Dónde se encontró", 140),
        "descripcion": ("Descripción", 200), "persona": ("Reportado por", 140), "correo": ("Correo", 200),
        "curso": ("Curso", 85), "fecha": ("Fecha", 95),
    }

    def __init__(self, padre, app):
        super().__init__(padre, app, [("Descartar", self.descartar, False),
                                      ("Recibido: agregar al listado", self.agregar, True)])

    def filas(self):
        return [(r["id"], (r["objeto"], r["categoria"], r["lugar"], r["descripcion"],
                           f"{r['nombre']} {r['apellido']}", r.get("correo", "—"), r["curso"], r["fecha"]))
                for r in reportes.pendientes(self.app.datos)]

    def agregar(self):
        reporte_id = self.seleccionado()
        if reporte_id is None or not messagebox.askyesno(
                "Agregar al listado", "¿Inspección ya recibió el objeto? Se agregará al listado como Disponible."):
            return
        nuevo = reportes.agregar_al_listado(self.app.datos, reporte_id)
        self.app.guardar()
        self.actualizar()
        self.avisar(f"«{nuevo['nombre']}» agregado al listado con el ID {nuevo['id']:02d}.")

    def descartar(self):
        reporte_id = self.seleccionado()
        if reporte_id is None or not messagebox.askyesno("Descartar", "¿Descartar este reporte?"):
            return
        reportes.descartar(self.app.datos, reporte_id)
        self.app.guardar()
        self.actualizar()
        self.avisar("Reporte descartado.")
